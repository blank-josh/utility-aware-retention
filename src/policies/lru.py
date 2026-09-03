"""
Person A: baseline policies. LRU is done as a reference for how to
implement the others (FIFO, LFU, CLOCK, ARC/LIRS-simplified, GreedyDual)
in this same file or sibling files (fifo.py, lfu.py, etc.) — one file
per policy keeps it clean for the paper's code appendix.
"""

from src.schema import Record


class LRUPolicy:
    def on_insert(self, buffer, new_record, capacity):
        if len(buffer) < capacity:
            return None
        # evict least-recently-used
        return min(buffer, key=lambda r: r.last_access)

    def on_access(self, record: Record) -> None:
        record.last_access = record.timestamp

    def name(self) -> str:
        return "LRU"
