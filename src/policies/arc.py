from src.schema import Record


class ARCPolicy:
    def __init__(self):
        self.recent = []
        self.frequent = []

    def on_insert(self, buffer, new_record, capacity):
        if len(buffer) < capacity:
            return None

        # Prefer evicting the least recently used record
        # from the recent list.
        if self.recent:
            victim_id = self.recent.pop(0)

            for record in buffer:
                if record.id == victim_id:
                    return record

        # Otherwise evict the least recently used
        # record from the frequent list.
        if self.frequent:
            victim_id = self.frequent.pop(0)

            for record in buffer:
                if record.id == victim_id:
                    return record

        # Fallback
        return buffer[0]

    def on_access(self, record: Record) -> None:
        record.access_count += 1
        record.last_access = record.timestamp

        if record.id in self.recent:
            self.recent.remove(record.id)
            self.frequent.append(record.id)
        elif record.id not in self.frequent:
            self.recent.append(record.id)

    def name(self) -> str:
        return "ARC"