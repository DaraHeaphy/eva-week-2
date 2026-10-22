"""Execute the inherited revision before extraction and capture its behaviour.

Requires Git and Matplotlib. Uses the immutable inherited commit, not the current
implementation. File saving/showing are intercepted; real plot construction runs.
"""
import contextlib
import io
import json
from pathlib import Path
import subprocess
from unittest.mock import patch

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
INHERITED = "9d535a37a1ee17ed5e72124cc8a83bf85b42b083"


def main():
    source = subprocess.run(["git", "show", INHERITED + ":evacodev2.py"],
                            cwd=ROOT, check=True, capture_output=True, text=True).stdout
    stdout = io.StringIO()
    namespace = {"__name__": "__main__"}
    with patch("builtins.input", return_value="USA") as prompt, \
         patch.object(plt, "show") as show, patch.object(plt, "savefig") as save, \
         contextlib.redirect_stdout(stdout):
        exec(compile(source, "inherited/evacodev2.py", "exec"), namespace)
    axes = plt.gca()
    baseline = {
        "revision": INHERITED, "country": "USA", "prompt": prompt.call_args.args[0],
        "stdout": stdout.getvalue(), "input_rows": len(namespace["eva_data"]),
        "prepared_rows": len(namespace["records"]),
        "dates": [date.isoformat() for date in namespace["dates"]],
        "cumulative_hours": namespace["cumulative_hours"],
        "country_hours": namespace["country_hours"],
        "xlabel": axes.get_xlabel(), "ylabel": axes.get_ylabel(),
        "output": save.call_args.args[0], "show_calls": show.call_count,
    }
    plt.close("all")
    output = ROOT / "docs/evidence/inherited-baseline.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(baseline, indent=2) + "\n", encoding="utf-8")
    print(f"Original executed: {baseline['input_rows']} input rows; {baseline['prepared_rows']} retained")
    print(baseline["stdout"], end="")


if __name__ == "__main__":
    main()
