"""Small repeatable benchmark for the CPU-bound extraction path."""

from pathlib import Path
import statistics
import sys
from time import perf_counter


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from skill_extractor import extract_skill_evidence, load_catalog  # noqa: E402


def measure(function, iterations=20):
    durations = []
    for _ in range(iterations):
        started = perf_counter()
        function()
        durations.append((perf_counter() - started) * 1000)
    return durations


def main():
    fixture = PROJECT_ROOT / "tests" / "fixtures" / "alphasense_excel_engineer.txt"
    text = fixture.read_text(encoding="utf-8")

    # Catalogue construction normally happens while importing app.py. Measure
    # only the warm extraction path that handles requests.
    load_catalog()
    durations = measure(
        lambda: extract_skill_evidence(text, source="job_description")
    )
    print(f"fixture: {fixture.name} ({len(text):,} characters)")
    print(f"iterations: {len(durations)}")
    print(f"median: {statistics.median(durations):.2f} ms")
    print(f"p95: {statistics.quantiles(durations, n=20)[18]:.2f} ms")


if __name__ == "__main__":
    main()
