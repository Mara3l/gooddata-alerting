from dataclasses import dataclass


@dataclass
class VisualizationThreshold:
    id: str
    column: str
    threshold: float
    threshold_type: str


@dataclass
class VisualizationThresholdCurrent(VisualizationThreshold):
    current: float


@dataclass
class ThresholdState:
    id: str
    notify: bool
    notified_before: bool
    last_update: str
