import csv
from fitness_analyzer.validation import validate_session_record, InvalidIdentifierError, InvalidRecordError

known_ids = {"P001", "P002", "P003"}

with open("data/fitness_sessions_invalid.csv", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

test_rows = [rows[0], rows[1], rows[6]]

for i, row in enumerate(test_rows, start=1):
    try:
        result = validate_session_record(row, i, "fitness_sessions_invalid.csv", known_ids)
        print("ACCEPTED:", result)
    except (InvalidIdentifierError, InvalidRecordError) as e:
        print("REJECTED:", e)
        