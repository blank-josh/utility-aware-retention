from src.schema import Record

class FIFOPolicy:
    def on_insert(self, buffer, new_record, capacity):
        if len(buffer) < capacity:
            return None
        return buffer[0]

    def on_access(self, record: Record) -> None:
        pass

    def name(self) -> str:
        return "FIFO"