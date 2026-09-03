"""
Shared contract for the whole project. Both of you import from this file —
do not redefine the record shape or policy interface anywhere else.
"""

from dataclasses import dataclass
from typing import Optional, Protocol


@dataclass
class Record:
    id: str
    timestamp: float
    value: float
    size: float = 1.0          # keep uniform (1.0) unless dataset gives real sizes
    importance: float = 0.0    # 0-1, derived from z-score/threshold at load time
    access_count: int = 0      # bump this on each "access" during simulation
    last_access: float = 0.0   # timestamp of most recent access


class EvictionPolicy(Protocol):
    """
    Every policy — baseline or ours — implements this exact interface so the
    simulator can swap policies in and out identically.
    """

    def on_insert(self, buffer: list[Record], new_record: Record, capacity: int) -> Optional[Record]:
        """
        Called when a new record arrives. If buffer is full, return the record
        to evict. Return None if no eviction is needed (buffer has room).
        Must NOT mutate buffer itself — simulator handles insert/evict.
        """
        ...

    def on_access(self, record: Record) -> None:
        """Called whenever a record is 'read' during simulation. Update any
        internal state (e.g. LRU order, LFU counts) here."""
        ...

    def name(self) -> str:
        """Short identifier used in logs/plots, e.g. 'LRU', 'UtilityAware'."""
        ...
