from src.schema import Record


class GreedyDualPolicy:
    def __init__(self):
        self.L = 0.0
        self.H = {}

    def on_insert(self, buffer, new_record, capacity):
        if len(buffer) < capacity:
            return None

        for record in buffer:
            size = max(record.size, 0.000001)
            self.H[record.id] = (1.0 / size) + self.L

        evict = min(buffer, key=lambda r: self.H.get(r.id, 0.0))

        self.L = self.H[evict.id]

        return evict

    def on_access(self, record: Record) -> None:
        record.last_access = record.timestamp

    def name(self) -> str:
        return "GreedyDual"