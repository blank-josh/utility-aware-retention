"""
Person A: metrics computed from a run_simulation() result dict.
"""

def retention_accuracy(sim_result: dict, all_records_importance_sum: float) -> float:
    retained_importance = sum(
        record.importance
        for record in sim_result["final_buffer"]
    )

    if all_records_importance_sum == 0:
        return 0.0

    return retained_importance / all_records_importance_sum


def high_utility_hit_ratio(
    sim_result: dict,
    importance_threshold: float = 0.7
) -> float:

    retained_high = sum(
        record.importance >= importance_threshold
        for record in sim_result["final_buffer"]
    )

    evicted_high = sum(
        entry["action"] == "evict"
        and entry["importance"] >= importance_threshold
        for entry in sim_result["log"]
    )

    total_high = retained_high + evicted_high

    if total_high == 0:
        return 0.0

    return retained_high / total_high


def overhead_per_decision(sim_result: dict) -> float:
    if "decision_times" not in sim_result:
        raise ValueError(
            "Simulation result does not contain decision timing data."
        )

    decision_times = sim_result["decision_times"]

    if not decision_times:
        return 0.0

    return sum(decision_times) / len(decision_times)