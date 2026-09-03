from src.schema import Record


class LFUPolicy:
    def on_insert(self, buffer, new_record, capacity):
        if len(buffer) < capacity:
            return None

        return min(
            buffer,
            key=lambda r: (r.access_count, r.last_access)
        )

    def on_access(self, record: Record) -> None:
        record.access_count += 1
        record.last_access = record.timestamp

    def name(self) -> str:
        return "LFU"