# EVA code handoff

This activity continues Kami's inherited EVA script at `9d535a3`. Existing code blocks
were extracted into functions; the record tuples, preparation policy, algorithms and
original graph/text operations remain. See the [source map](docs/INHERITED-SOURCE-MAP.md).

## Setup and original operation

Python 3.10+; run from this repository directory because original file paths are relative
to the working directory:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python evacodev2.py
```

Enter a dataset country label, such as USA or Russia. The inherited case-insensitive
country query prints total hours. The global cumulative chart is saved to
cumulative_duration.png and displayed. The original dataset is unchanged.
Dependencies are compatible-range specified, not locked. Verified environment:
Python 3.11.9 and Matplotlib 3.8.3. A clean-environment installation is not claimed.

## Tests and source extraction checks

```powershell
python -B -m unittest discover -v
python -B tools/check_extraction.py
```

Analysis tests can use in-memory tuples without terminal, files or Matplotlib.
Application/plot tests use Matplotlib's Agg backend and intercept window display.
To re-execute the original revision and capture its baseline, use
`python -B tools/capture_inherited_baseline.py` from the repository root (requires Git).

## Handoff documents

- [Initial assessment](docs/INITIAL-ASSESSMENT.md)
- [Module diagram and contracts](docs/ARCHITECTURE.md)
- [Source map](docs/INHERITED-SOURCE-MAP.md)
- [ADR-001](docs/ADR-001.md)

Implementation and documentation were prepared with Codex assistance.

## Required country comparison

```powershell
python evacodev2.py --compare USA Russia --start-year 1965 --end-year 2013
python evacodev2.py --compare USA Russia --start-year 1900 --end-year 1901
python -B tools/verify.py
```

Years include both endpoints. The comparison reports event-entry count, total/mean
hours and winner/tie. Known countries with no matches produce zero count/total and
unavailable average. Unknown countries, reversed/missing/out-of-range years, nonnumeric
years and year flags without comparison give an explanatory error and exit 2.
Country input is case insensitive and comparison trims outer spaces. Available labels
come from all prepared records, before year filtering. Comparison does not prompt or
open a graph; no-argument invocation keeps the original workflow unchanged.

45 of 375 source rows lack date or duration and are skipped by the original policy.
Dated zero-duration entries count. Results describe retained dataset entries, not
necessarily completed EVAs or complete historical activity. Source data and old
validation behaviour are unchanged; stronger validation would be separate work.

- [ADR-002](docs/ADR-002.md): comparison decisions and alternatives.
- [Evaluation and requirement map](docs/EVALUATION.md).
- [Recorded test/extraction/smoke evidence](docs/evidence/verification.txt).

History separates assessment/plan, inherited-code extraction and new functionality.
Use `git log --oneline` to locate each dedicated commit.
Personal interview notes and learning exercises remain local and are excluded from Git.
