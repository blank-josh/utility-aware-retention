"""
Person B: core simulation engine. Runs a stream of Records through a given
EvictionPolicy at a fixed capacity and logs every retain/evict decision.
"""

from src.schema import Record, EvictionPolicy


def run_simulation(stream: list[Record], policy: EvictionPolicy, capacity: int) -> dict:
    buffer: list[Record] = []
    log = []  # list of dicts: {timestamp, action, record_id, importance}

    for record in stream:
        evict_target = policy.on_insert(buffer, record, capacity)
        if evict_target is not None:
            buffer.remove(evict_target)
            log.append({
                "timestamp": record.timestamp,
                "action": "evict",
                "record_id": evict_target.id,
                "importance": evict_target.importance,
            })
        buffer.append(record)
        policy.on_access(record)
        log.append({
            "timestamp": record.timestamp,
            "action": "retain",
            "record_id": record.id,
            "importance": record.importance,
        })

    return {
        "policy": policy.name(),
        "capacity": capacity,
        "final_buffer": buffer,
        "log": log,
    }
