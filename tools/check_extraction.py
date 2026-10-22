"""Check original statement ASTs against extracted functions, beyond output equality."""
import ast
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
REVISION = "9d535a37a1ee17ed5e72124cc8a83bf85b42b083"


def check():
    original = subprocess.run(["git", "show", REVISION + ":evacodev2.py"], cwd=ROOT,
                              check=True, capture_output=True, text=True).stdout
    def block(start, end=None):
        source = original[original.index(start):original.index(end) if end else None]
        return ast.parse(source.strip()).body
    def body(filename, name):
        tree = ast.parse((ROOT / filename).read_text(encoding="utf-8"))
        function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name)
        return [node for node in function.body if not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str))]
    def equal(first, second):
        return [ast.dump(node) for node in first] == [ast.dump(node) for node in second]
    loading = original[original.index('with open('):original.index('\nrecords = []')].replace('open("eva-data.json",', 'open(filename,')
    results = {
        "loading_unchanged_except_filename_parameter": equal(ast.parse(loading).body, body("eva_loading.py", "load_eva_data")[:-1]),
        "preparation_statements_unchanged": equal(block("records = []", "\ndates = []"), body("eva_preparation.py", "prepare_records")[:-1]),
        "cumulative_statements_unchanged": equal(block("dates = []", "\nselected_country = input"), body("eva_analysis.py", "cumulative_duration")[:-1]),
        "country_sum_unchanged": equal(block("country_hours = sum", "\nprint("), body("eva_analysis.py", "total_duration_for_country")[:-1]),
        "country_print_unchanged": equal(block('print(', "\n\nplt.plot"), body("eva_presentation.py", "display_country_total")),
        "plot_statements_unchanged": equal(block("plt.plot("), body("eva_presentation.py", "plot_cumulative_duration")[1:]),
    }
    print(json.dumps(results, indent=2))
    if not all(results.values()):
        raise SystemExit("An inherited block changed beyond the documented extraction")
    return results


if __name__ == "__main__":
    check()
