# Utility-Aware Retention Policy — Implementation

Companion repo to "A Loss-Tolerant, Utility-Aware Retention Policy for
Time-Series Telemetry in Resource-Constrained Systems" (G Joshika, Sneh
Dongle). Target venue: InC4 2026 / INDIACom-2026.

## Structure

```
data/                   raw + processed datasets (gitignored if large)
src/
  schema.py             Record dataclass + EvictionPolicy interface — THE CONTRACT
  data_loader.py         [Person A] load CSV, derive importance labels
  policies/
    lru.py                [Person A] baseline (reference implementation, done)
    fifo.py, lfu.py, ...   [Person A] add one file per baseline policy
    utility_aware.py       [Person B] our proposed policy
  simulation/
    simulator.py            [Person B] core run loop
    metrics.py               [Person A] retention accuracy, hit ratio, overhead
notebooks/               Colab notebooks for exploration + demo running
results/
  plots/                    output charts
  logs/                     raw simulation logs (for later ablations)
paper/                    LaTeX/Overleaf source, kept in sync with results
tests/                    quick sanity tests per policy
```

## The contract (read this first, both of you)

Everything imports `Record` and the `EvictionPolicy` interface from
`src/schema.py`. Do not redefine the record shape elsewhere — if you need
a new field, add it to `schema.py` and tell the other person.

## Split

**Person A — data & baselines & metrics**
- `src/data_loader.py` — finalize importance derivation logic
- `src/policies/` — FIFO, LFU, CLOCK, GreedyDual, and a simplified ARC or
  LIRS (pick one for the demo; note in code comments which parts are
  simplified vs. full — you'll need this note for the paper later)
- `src/simulation/metrics.py` — retention accuracy, hit ratio, overhead
- `results/plots/` — comparison bar charts once metrics are in

**Person B — our policy & engine**
- `src/policies/utility_aware.py` — fill in the utility score normalization
  and the adaptive threshold logic
- `src/simulation/simulator.py` — core loop, extend with load simulation
  (synthetic signal if dataset has none) and timing instrumentation for
  overhead metric
- `notebooks/` — the Colab notebook that ties data → policies → simulator →
  metrics → plots together end to end

## Roadmap (post-tomorrow, toward Nov 20 submission)

1. Tomorrow: pilot run, one dataset, simplified baselines — proof of concept
2. Swap simplified ARC/LIRS for full implementations
3. Add 1–2 more datasets from a different telemetry domain
4. Capacity sweep (5%–50%) instead of single budget, plotted as curves
5. Multi-run statistics (mean ± std across random stream orderings)
6. Weight sensitivity analysis / learned weights for the utility function
7. Write Methodology + Evaluation sections against the strengthened results

## Setup

```bash
pip install pandas numpy matplotlib
```

Run the demo notebook in `notebooks/` or import directly:

```python
from src.data_loader import load_telemetry
from src.policies.lru import LRUPolicy
from src.simulation.simulator import run_simulation

records = load_telemetry("data/telemetry.csv", value_col="value")
result = run_simulation(records, LRUPolicy(), capacity=50)
```
