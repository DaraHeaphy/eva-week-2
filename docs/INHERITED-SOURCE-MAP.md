# Source map from the inherited application

Original: `git show 9d535a3:evacodev2.py`. Line numbers below refer to that revision.
The extracted functions keep the original statements and tuple representation.

| Original lines | Destination | Necessary extraction changes |
|---|---|---|
| 5-6: open/load JSON | eva_loading.load_eva_data | filename becomes an argument with the same default; return eva_data |
| 8-23: checks/conversion/append/sort | eva_preparation.prepare_records | wrap in function accepting eva_data; return records |
| 25-32: running cumulative loop | eva_analysis.cumulative_duration | wrap in function accepting records; return dates/cumulative_hours |
| 35: country sum | eva_analysis.total_duration_for_country | wrap in function accepting records/selected_country; return country_hours |
| 36: print total | eva_presentation.display_country_total | wrap in function accepting selected_country/country_hours |
| 38-43: pyplot calls | eva_presentation.plot_cumulative_duration | wrap with dates/cumulative_hours arguments; Matplotlib imported inside plotting |
| 34: country prompt | evacodev2.main | retained verbatim, surrounded by calls to the extracted blocks |

Imports follow the operations that use them. A main guard prevents import-time effects.
No domain class, different record shape, changed missing-field policy, alternative
calculation or new plotting implementation was introduced. Default working-directory
input/output paths remain the same as the inherited script.

`python -B tools/check_extraction.py` compares the original statement ASTs to the
extracted function bodies. It ignores indentation, positions, comments and docstrings,
but checks the operations, variables, literals and expressions. The sole allowed loading
substitution is the filename parameter. It checks provenance, not complete correctness.
The separate baseline and known-answer tests check behaviour. Together these give
stronger evidence than saying a replacement happens to produce the same total.
