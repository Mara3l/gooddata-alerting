import os
import schedule
import time

import yaml
from gooddata_pandas import GoodPandas

from services.notification import Notification
from utils.gooddata_types import VisualizationThreshold, VisualizationThresholdCurrent
from services.state import State
from services.comparator import Comparator

gooddat_host = os.getenv("GOODDATA_HOST")
gooddata_token = os.getenv("GOODDATA_TOKEN")
gooddata_workspace_id = os.getenv("GOODDATA_WORKSPACE_ID")
bucket_name = os.getenv("S3_BUCKET_NAME")
email_passowrd = os.getenv("EMAIL_PASSWORD")
directory_name = "alerting"

gp = GoodPandas(gooddat_host, gooddata_token)
frames = gp.data_frames(gooddata_workspace_id)


# the function loads gooddata_thresholds.yaml and returns list of VisualizationThreshold dataclasses
def get_thresholds() -> list[VisualizationThreshold]:
    visualization_thresholds = []

    with open("thresholds/gooddata_thresholds.yaml", "r") as file:
        thresholds_definition = yaml.safe_load(file)

    for threshold in thresholds_definition["visualizations"]:
        visualization_thresholds.append(
            VisualizationThreshold(
                threshold["id"],
                threshold["column"],
                threshold["threshold"],
                threshold["threshold_type"])
        )

    return visualization_thresholds


# the function loads all values from visualizations defined in gooddata_thresholds.yaml
# and returns list of VisualizationThreshold dataclasses
def get_current_thresholds(
        visualization_thresholds: list[VisualizationThreshold]
) -> list[VisualizationThresholdCurrent]:
    visualization_current_thresholds = []

    for visualization_threshold in visualization_thresholds:
        df = frames.for_insight(visualization_threshold.id)
        visualization_current_thresholds.append(
            VisualizationThresholdCurrent(
                visualization_threshold.id,
                visualization_threshold.column,
                visualization_threshold.threshold,
                visualization_threshold.threshold_type,
                # get current value of a visualization
                df[visualization_threshold.column][0]
            )
        )

    return visualization_current_thresholds


def main():
    state = State(bucket_name, "alerting")
    notification = Notification(
        "patrik.braborec@gooddata.com",
        "patrik.braborec@gooddata.com",
        "smtp.gmail.com",
        email_passowrd
    )
    comparator = Comparator()

    thresholds = get_thresholds()
    current_thresholds = get_current_thresholds(thresholds)
    old_state = state.load_state() if state.has_state() else []
    new_state = comparator.compute(current_thresholds)
    old_dict = {item.id: item for item in old_state}
    new_dict = {item.id: item for item in new_state}

    for new_id, new_item in new_dict.items():
        old_item = old_dict.get(new_id)

        if old_item:
            if new_item.notify and not old_item.notified_before:
                notification.send_email("Alert!", f"Visualization with id {new_item.id} has reached threshold!")
                new_item.notified_before = True

            if old_item.notified_before and new_item.notify:
                new_item.notified_before = True

            if old_item.notified_before and not new_item.notify:
                new_item.notified_before = False
        else:
            if new_item.notify:
                notification.send_email("Alert!", f"Visualization with id {new_item.id} has reached threshold!")
                new_item.notified_before = True

    state.create_or_update_state(new_dict.values())


main()

schedule.every().day.at("08:00").do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
