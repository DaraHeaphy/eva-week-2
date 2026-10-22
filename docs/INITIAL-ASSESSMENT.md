# Assessment of the inherited EVA application

The inherited starting point is Kami's commit `9d535a3` (full hash in the captured
baseline). It added the country-total query on top of the earlier cumulative graph.
The two previous commits are `f067396` and `b08274d`. The application changes
build directly on the inherited revision, whose commits remain unchanged.

## Existing behaviour and dependencies

`evacodev2.py` is the only source module. At top level it opens eva-data.json relative
to the working directory; prepares (datetime, float hours, country) tuples; skips rows
with missing/empty date or duration; sorts tuples by date; accumulates global running
hours; asks `Country: `; calculates the case-insensitive country sum; prints two decimal
hours; plots the global cumulative series; labels, tightens, saves and shows it.
The saved name is cumulative_duration.png. The chart is cumulative at each record,
not an independent annual total and not astronaut-hours multiplied by crew size.

File reading, preparation, analysis, presentation and execution are mixed in one unit.
The country calculation and cumulative loop share global tuples. Importing calculations
also reads a file, prompts and displays a graph. A change to tuple layout affects both
analyses. These implicit contracts and effects make isolated tests difficult. There is
little duplicated algorithm in the inherited script; the concern is responsibility
boundaries, not a claim that all original code is poor.

## Execute before restructuring

Ran `python -B tools/capture_inherited_baseline.py` against the inherited original.
The helper executes source from the immutable inherited revision with USA input and
Agg plotting. It intercepts save/show calls but runs the original calculations and
plot construction. This is automated execution, not a manually exercised GUI session.
`evidence/inherited-baseline.json` captures all points, prompt, stdout, labels, output
filename and show count. 375 input rows yield 330 retained records, USA 1257.13 hours.

## Data interpretation and boundaries

The JSON array contains EVA event entries, with varying eva, country, crew, vehicle,
date, duration and purpose fields. Dates are ISO year-month-day timestamps; durations
are interpreted as hours:minutes by the inherited conversion. Several crew names may
occur in a row. Country labels do not establish every crew member's nationality.
45 rows lack a date or duration and are skipped. Some dated entries have zero duration
and may describe cancelled activity. Numeric results therefore describe retained entries,
not guaranteed complete historical counts. Purpose-text encoding artifacts are outside
these calculations. The extraction preserves this data and these existing preparation rules.
