from datetime import datetime

from utils.gooddata_types import ThresholdState, VisualizationThresholdCurrent


class Comparator:
    def compute(
            self,
            visualization_threshold_current: list[VisualizationThresholdCurrent]
    ) -> list[ThresholdState]:
        new_state = []

        for threshold in visualization_threshold_current:
            if threshold.threshold_type == "uptrends":
                new_state.append(ThresholdState(
                    threshold.id,
                    True if threshold.current > threshold.threshold else False,
                    # for new state, 'notified_before' is always False
                    False,
                    datetime.today().strftime("%Y-%m-%d"),
                ))
            elif threshold.threshold_type == "downtrends":
                new_state.append(ThresholdState(
                    threshold.id,
                    True if threshold.current < threshold.threshold else False,
                    # for new state, 'notified_before' is always False
                    False,
                    datetime.today().strftime("%Y-%m-%d"),
                ))
            else:
                print(f"unknown 'threshold_type' {threshold.threshold_type}")

        return new_state
