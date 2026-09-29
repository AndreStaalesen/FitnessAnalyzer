import csv

with open("data/participants.csv", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)


print("\nFITNESS SESSIONS (valid):")
with open("data/fitness_sessions.csv", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)


print("\nFITNESS SESSIONS (invalid):")
with open("data/fitness_sessions_invalid.csv", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)

        