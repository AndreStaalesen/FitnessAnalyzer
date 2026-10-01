import csv
from pathlib import Path

from fitness_analyzer.analysis_utils import describe_classification


def ensure_output_dir(output_dir):
    Path(output_dir).mkdir(parents=True, exist_ok=True)


def write_analysis_summary(sessions, output_dir):
    path = Path(output_dir) / "analysis_summary.csv"
    fieldnames = [
        "session_id", "participant_id", "total_observations", "valid_observations",
        "average_heart_rate", "min_heart_rate", "max_heart_rate",
        "average_activity_level", "min_activity_level", "max_activity_level",
        "average_skin_response_difference", "average_temperature_difference", "classification",
    ]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for session in sessions:
            writer.writerow(session.to_dict())


def write_analysis_report(sessions, output_dir):
    path = Path(output_dir) / "analysis_report.txt"
    with open(path, "w", encoding="utf-8") as f:
        for session in sessions:
            f.write(f"Session {session.session_id} - Participant {session.participant.participant_id}\n")
            f.write(f"Observations used: {session.valid_observation_count}/{session.total_observations}\n")
            f.write(f"Average heart rate: {session.average_heart_rate()}\n")
            f.write(f"Average activity level: {session.average_activity_level()}\n")
            f.write(f"Classification: {session.classify()}\n")
            f.write(f"{describe_classification(session.classify())}\n")
            f.write("-" * 40 + "\n")


def write_rejected_records(rejected_records, output_dir):
    path = Path(output_dir) / "rejected_records.txt"
    with open(path, "w", encoding="utf-8") as f:
        if not rejected_records:
            f.write("No rejected records.\n")
        for reason in rejected_records:
            f.write(reason + "\n")