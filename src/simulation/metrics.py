"""
Person A: metrics computed from a run_simulation() result dict.
"""


def retention_accuracy(sim_result: dict, all_records_importance_sum: float) -> float:
    """Sum of importance of records retained in final buffer / total importance in stream."""
    retained_importance = sum(r.importance for r in sim_result["final_buffer"])
    return retained_importance / all_records_importance_sum if all_records_importance_sum else 0.0


def high_utility_hit_ratio(sim_result: dict, importance_threshold: float = 0.7) -> float:
    """% of high-importance records still in buffer at end of stream."""
    final_ids = {r.id for r in sim_result["final_buffer"]}
    evicted_high = [e for e in sim_result["log"]
                    if e["action"] == "evict" and e["importance"] >= importance_threshold]
    retained_high = [r for r in sim_result["final_buffer"] if r.importance >= importance_threshold]
    total_high = len(retained_high) + len(evicted_high)
    return len(retained_high) / total_high if total_high else 0.0


def overhead_per_decision(sim_result: dict) -> float:
    """Placeholder — wrap policy.on_insert calls with timing in the simulator
    if you want real wall-clock overhead numbers."""
    raise NotImplementedError
