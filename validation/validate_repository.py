from pathlib import Path
import json
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
required = [
    "README.md",
    "project.json",
    "LICENSE",
    "CITATION.cff",
    "requirements.txt",
    "assets/project-cover.png",
    "assets/repository-social-preview.png",
    "data/processed/tables/Final_Project_Key_Results.csv",
    "data/processed/tables/Publication_Table_01_Final_Settlement_Results.csv",
    "outputs/maps/02_final_settlement_evidence_classification.png",
    "outputs/figures/figure_01_final_decision_distribution.png",
    "scripts/python/reproduce_summary.py",
]

failures = [f"Missing: {item}" for item in required if not (ROOT/item).exists()]

for path in ROOT.rglob("*"):
    if path.is_file() and path.stat().st_size > 24 * 1024 * 1024:
        failures.append(f"Browser-upload limit exceeded: {path.relative_to(ROOT)}")

try:
    meta = json.loads((ROOT/"project.json").read_text(encoding="utf-8"))
    if meta["settlements_screened"] != 2455:
        failures.append("Unexpected settlements-screened metadata")
except Exception as exc:
    failures.append(f"Invalid metadata: {exc}")

try:
    decisions = pd.read_csv(ROOT/"data/processed/tables/Publication_Table_02_Decision_Distribution.csv")
    if int(decisions["Settlement_Count"].sum()) != 13:
        failures.append("Final decision counts do not sum to 13")
except Exception as exc:
    failures.append(f"Could not validate decision distribution: {exc}")

if failures:
    print("REPOSITORY VALIDATION: FAILED")
    for failure in failures:
        print("-", failure)
    sys.exit(1)

print("REPOSITORY VALIDATION: PASSED")
print("Required files, result counts and browser-upload limits are valid.")
