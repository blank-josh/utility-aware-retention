# Utility-Aware Retention Policy for Time-Series Telemetry

A loss-tolerant, utility-aware retention/eviction policy for
resource-constrained time-series telemetry systems, benchmarked
against LRU, FIFO, LFU, CLOCK, GreedyDual, and simplified ARC.

## Pilot Results (N=2000, 10% capacity)

| Policy       | Retention Accuracy | High-Utility Hit Ratio |
|--------------|--------------------:|------------------------:|
| LRU          | 0.1035              | 0.00                    |
| FIFO         | 0.1035              | 0.00                    |
| LFU          | 0.1035              | 0.00                    |
| CLOCK        | 0.1062              | 0.00                    |
| GreedyDual   | 0.1035              | 0.00                    |
| ARC (simpl.) | 0.1035              | 0.00                    |
| UtilityAware | **0.2214**          | **1.00**                |

Full methodology, results, and limitations discussion in
`notebooks/end_to_end.ipynb`.

## Structure
- `src/schema.py` — shared Record/EvictionPolicy contract
- `src/data_loader.py` — dataset loading + importance derivation
- `src/policies/` — baseline and proposed eviction policies
- `src/simulation/` — simulator engine + evaluation metrics
- `notebooks/end_to_end.ipynb` — full pipeline, results, discussion
- `results/` — output CSV and plots

## Authors
G Joshika, Sneh Dongle — target venue: InC4 2026 / INDIACom-2026
