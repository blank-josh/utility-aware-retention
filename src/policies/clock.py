from src.schema import Record


class CLOCKPolicy:
    def __init__(self):
        self.hand = 0
        self.reference_bits = {}

    def on_insert(self, buffer, new_record, capacity):
        if len(buffer) < capacity:
            return None

        while True:
            if self.hand >= len(buffer):
                self.hand = 0

            record = buffer[self.hand]

            if self.reference_bits.get(record.id, 0) == 0:
                evict = record
                self.hand = (self.hand + 1) % len(buffer)
                return evict

            self.reference_bits[record.id] = 0
            self.hand = (self.hand + 1) % len(buffer)

    def on_access(self, record: Record) -> None:
        self.reference_bits[record.id] = 1
        record.last_access = record.timestamp

    def name(self) -> str:
        return "CLOCK"