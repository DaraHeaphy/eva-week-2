"""Reproduce extraction checks, tests and original/new CLI smoke runs."""
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent


def main():
    env = dict(os.environ, MPLBACKEND="Agg", PYTHONDONTWRITEBYTECODE="1")
    commands = [
        (["tools/check_extraction.py"], 0, None),
        (["-m", "unittest", "discover", "-v"], 0, None),
        (["evacodev2.py"], 0, "USA\n"),
        (["evacodev2.py", "--compare", "USA", "Russia", "--start-year", "1965", "--end-year", "2013"], 0, None),
        (["evacodev2.py", "--compare", "USA", "Russia", "--start-year", "1900", "--end-year", "1901"], 0, None),
        (["evacodev2.py", "--compare", "Mars", "USA", "--start-year", "2000", "--end-year", "2001"], 2, None),
        (["evacodev2.py", "--compare", "USA", "Russia", "--start-year", "2010", "--end-year", "2000"], 2, None),
        (["evacodev2.py", "--compare", "USA", "Russia", "--start-year", "bad", "--end-year", "2000"], 2, None),
    ]
    evidence = [f"Python {sys.version.split()[0]}; Matplotlib backend Agg\n"]
    failures = 0
    for args, expected, stdin in commands:
        result = subprocess.run([sys.executable, "-B", *args], cwd=ROOT, env=env,
                                input=stdin, capture_output=True, text=True)
        evidence.extend(["$ python -B " + " ".join(args) + "\n", result.stdout, result.stderr,
                         f"Exit: {result.returncode}; expected: {expected}\n\n"])
        failures += result.returncode != expected
    output = ROOT / "cumulative_duration.png"
    valid_png = output.exists() and output.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
    failures += not valid_png
    evidence.append(f"Original output is PNG: {valid_png}\nVerification failures: {failures}\n")
    (ROOT / "docs/evidence/verification.txt").write_text("".join(evidence), encoding="utf-8")
    print("".join(evidence))
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
