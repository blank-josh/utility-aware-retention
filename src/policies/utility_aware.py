"""
Person B: our proposed policy. Implements the EvictionPolicy interface
from src/schema.py.
"""

from src.schema import Record


class UtilityAwarePolicy:
    def __init__(self, w_recency=0.25, w_frequency=0.25, w_importance=0.35, w_load=0.15):
        self.w_recency = w_recency
        self.w_frequency = w_frequency
        self.w_importance = w_importance
        self.w_load = w_load
        self.current_load = 0.0  # 0-1, updated externally by simulator each step

    def utility_score(self, record: Record, now: float) -> float:
        # TODO: normalize each term to 0-1 before combining
        recency_score = 1.0  # placeholder: 1 / (now - record.last_access + eps)
        frequency_score = 1.0  # placeholder: normalize record.access_count
        importance_score = record.importance
        load_penalty = self.current_load  # higher load -> lower tolerance for low-utility records

        return (
            self.w_recency * recency_score
            + self.w_frequency * frequency_score
            + self.w_importance * importance_score
            - self.w_load * load_penalty
        )

    def on_insert(self, buffer, new_record, capacity):
        if len(buffer) < capacity:
            return None
        # evict lowest-utility record
        scored = [(self.utility_score(r, new_record.timestamp), r) for r in buffer]
        scored.sort(key=lambda x: x[0])
        return scored[0][1]

    def on_access(self, record: Record) -> None:
        record.access_count += 1
        record.last_access = record.timestamp

    def name(self) -> str:
        return "UtilityAware"
