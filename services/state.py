import boto3
import yaml

from utils.gooddata_types import ThresholdState


class State:
    def __init__(self, bucket_name: str, folder_name: str):
        self.bucket_name = bucket_name
        self.folder_name = folder_name
        self.s3_client = boto3.client('s3')
        self.s3_resources = boto3.resource("s3")
        self.s3_key = f"/{self.folder_name}/gooddata_state.yaml"

    def has_state(self):
        try:
            self.s3_client.get_object(Bucket=self.bucket_name, Key=self.s3_key)
            return True
        except self.s3_client.exceptions.NoSuchKey:
            return False

    def remove_state(self):
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=self.s3_key)

    def load_state(self) -> list[ThresholdState]:
        response = self.s3_client.get_object(Bucket=self.bucket_name, Key=self.s3_key)
        state = yaml.safe_load(response["Body"].read())
        deserialized_state = []

        for item in state["visualizations"]:
            deserialized_state.append(ThresholdState(
                item["id"],
                item["notify"],
                item["notified_before"],
                item["last_update"]
            ))

        return deserialized_state

    def create_or_update_state(self, state: list[ThresholdState]):
        serialized_state = {
            "visualizations": []
        }

        for item in state:
            serialized_state["visualizations"].append({
                "id": item.id,
                "notify": item.notify,
                "notified_before": item.notified_before,
                "last_update": item.last_update,
            })

        self.s3_client.put_object(Body=yaml.dump(serialized_state), Bucket=self.bucket_name, Key=self.s3_key)
