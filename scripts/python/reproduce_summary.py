from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "data" / "processed" / "tables"

key = pd.read_csv(TABLES / "Final_Project_Key_Results.csv")
values = dict(zip(key["Metric"], key["Value"]))

expected = {
    "Settlements screened": "2455",
    "LGAs covered": "27",
    "Detailed validation cases": "13",
    "Probable abandonment": "5",
    "Possible abandonment": "1",
    "Uncertain": "4",
    "Not supported": "2",
    "Reconstruction or reoccupation": "1",
    "Confirmed abandonment": "0",
    "Highest-ranked settlement": "Wumbi",
    "Highest-ranked LGA": "Kala Balge",
}

for metric, expected_value in expected.items():
    actual = str(values[metric])
    if actual != expected_value:
        raise ValueError(f"{metric}: expected {expected_value}, found {actual}")

decisions = pd.read_csv(TABLES / "Publication_Table_02_Decision_Distribution.csv")
if int(decisions["Settlement_Count"].sum()) != 13:
    raise ValueError("Decision distribution does not sum to 13")

print("RESULT REPRODUCTION: PASSED")
print("Settlements screened: 2,455")
print("Detailed validation cases: 13")
print("Probable abandonment: 5")
print("Possible abandonment: 1")
print("Uncertain: 4")
print("Confirmed abandonment: 0")
