# Activity verification and maintainability evaluation

## Traceability to Week 6

Source: SWA/slides/SAW6-2026-27.pdf, Week 6 overview, handoff and Activities 1-6.
This implements the individual inherited-code handoff, not a replacement application.

| Requirement | Evidence |
|---|---|
| Receive and work with inherited code | Starting point 9d535a3; original blocks retained, INHERITED-SOURCE-MAP.md |
| Preserve Git history | All inherited commits through 9d535a3 remain unchanged ancestors of the activity commits |
| Examine and execute before changes | INITIAL-ASSESSMENT.md, capture helper and inherited-baseline.json; the assessment/plan commit precedes extraction |
| AR1 separation; AR2 modules; AR4 cohesion | Four focused modules plus existing executable coordinator; ARCHITECTURE.md |
| AR3 low coupling/interfaces | Functions communicate through inherited tuple lists and explicit arguments/returns; no responsibility-module imports another |
| AR5 preserve behaviour | Exact original-statement extraction check; baseline chart/output/prompt/labels/save/show checks |
| Activity 2 / AR7 first ADR and diagram | ADR-001.md and ARCHITECTURE.md |
| Activity 3 separately committed extraction | Dedicated extraction commit; five tests passed before adding comparison |
| Activity 4 comparison | compare_countries, display_comparison and optional flags on existing coordinator |
| AR6 / Activity 5 tests/evaluation/second ADR | tests/, verification record, this document and ADR-002.md |
| Activity 6 runnable documented handoff | README setup/run/tests; local commits; no study files included |

## What was retained, moved and added

Retained: original JSON bytes; tuple shape and variable names; skip checks; ISO
conversion; hours + minutes/60; append/sort; cumulative loop; country sum; original
input text, printed total, pyplot calls, file names and working-directory behaviour.
Moved: operations wrapped into functions grouped by responsibility with arguments and
returns replacing globals. Matplotlib import is inside plotting. Added: main guard,
comparison flags/function/output, tests and activity documentation. No class model,
replacement plotting API or stricter preparation validation was introduced.

`tools/check_extraction.py` compares original and extracted Python statement trees.
Six checks pass: loading (filename parameter only), preparation, cumulative analysis,
country sum, country printing and plotting. It verifies source continuity, not all
semantic properties. Known-answer and characterization tests separately verify behaviour.

## Before and after comparison

| Question | Before | After and limitation |
|---|---|---|
| Responsibilities visible? | Five concerns at top level in one module | Four responsibility modules plus original coordinator; extra files need navigation |
| Dependencies? | Shared globals; importing computation performs I/O | Coordinator imports focused functions; tuple contract remains shared coupling |
| Add comparison? | Would mix new logic into original script | Three existing modules extended: analysis, presentation, coordinator; two loading/preparation modules unchanged |
| Independent tests? | No tests supplied; import prompts/plots | Pure functions accept known tuples without files/display; boundary tests still need integration setup |
| Duplication? | Little original duplication | Reuses inherited country sum; no claim of substantial duplication removal |
| Complexity cost? | Short script with implicit interfaces | Function wrappers/contracts/tests; no framework, classes or network layers |

18 tests pass. They check original known cumulative/country values; tuple preparation,
chronology and skips; inherited malformed-value handling; exact 330 original points;
prompt/text/labels/save/show; inclusive/single-year comparisons; count/total/average;
empty selections; tie and float noise; zero durations; unknown labels; invalid ranges;
controlled CLI responses; and imports without Matplotlib. The extraction stage passed
five tests before the new functionality was added. `docs/evidence/verification.txt`
records final commands and outcomes; `python -B tools/verify.py` reproduces them.

Baseline 375 input rows -> 330 retained; full 1965-2013 comparison: USA 217 entries,
1257.13 h, average 5.79 h; Russia 113 entries, 527.90 h, average 4.67 h. USA wins.
Tests and smoke runs used Python 3.11.9, Matplotlib 3.8.3 and Agg. Original no-argument
application also writes the real PNG in the smoke run. A graphical window and a fresh
dependency installation were not manually tested. No coverage or speedup measurement.

## Maintainability under ISO/IEC 25010:2023

Clause 3.7 concerns effective/efficient modification by intended maintainers. The brief
paraphrases below use the [GSO adoption of ISO/IEC 25010:2023, clauses 3.7-3.7.5](https://gso-sims-preview-doc-aws.s3-eu-west-1.amazonaws.com/gso-iso-iec-25010-2025-en.html).

| Subcharacteristic | Mechanism and observed evidence | Limit |
|---|---|---|
| Modularity | Limits change propagation: comparison leaves reading/preparation unchanged | Tuple changes still affect consumers |
| Reusability | Functions can serve other callers/assets; new query reuses inherited country sum | No production reuse in another system demonstrated |
| Analysability | Named boundaries, source map and ADRs identify causes/change locations | No timed developer study |
| Modifiability | Isolated extension with regression evidence supports change without damaging existing quality | Tests are evidence, not proof of zero defects |
| Testability | Explicit inputs/outputs enable objective in-memory known-answer tests | File/plot integration remains separate work |

Boundaries reduce the code to inspect (analysability); pure functions make assertions
feasible (testability); both support safer modification. These are distinct qualities
with interacting effects. More files alone do not demonstrate improvement. No ISO
certification, percentage score or maintenance-time improvement is claimed.

## Limits and next steps

Existing input assumptions remain deliberately: malformed present dates/durations may
raise, country fields can be absent, and the original conversion accepts unusual minute
values. Extraction tests document preservation rather than endorse data quality. A
future validation policy should be agreed and tested separately. 45 rows are skipped
as before; missing dates cannot be assigned to a period. Zero-duration entries may be
cancellations. Clarify scientific eligibility before changing counts; do not silently
revise historic totals. Country labels known only in excluded rows are unavailable to
comparison. Dictionary summaries are simple but positional tuple and result contracts
need care. A measured change task, broader fixtures and environment locking could
corroborate improvements if justified by future requirements.
