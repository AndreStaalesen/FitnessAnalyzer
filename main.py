import argparse
from pathlib import Path

from fitness_analyzer.loader import load_participants, load_sessions, build_sessions
from fitness_analyzer.report_writer import (
    ensure_output_dir,
    write_analysis_summary,
    write_analysis_report,
    write_rejected_records,
)


def parse_args():
    parser = argparse.ArgumentParser(description="Smart Fitness Session Analyzer")
    parser.add_argument("--profiles", required=True, help="Path to the participants CSV file")
    parser.add_argument("--sessions", required=True, help="Path to the fitness sessions CSV file")
    parser.add_argument("--output", required=True, help="Directory to write report files into")
    return parser.parse_args()


def derive_invalid_path(sessions_path):
    path = Path(sessions_path)
    return path.with_name(path.stem + "_invalid" + path.suffix)


def run(profiles_path, sessions_path, output_dir):
    participants = load_participants(profiles_path)
    known_ids = set(participants.keys())

    accepted, rejected = load_sessions(sessions_path, known_ids)

    invalid_path = derive_invalid_path(sessions_path)
    if invalid_path.exists():
        accepted_invalid, rejected_invalid = load_sessions(str(invalid_path), known_ids)
        accepted += accepted_invalid
        rejected += rejected_invalid

    sessions = build_sessions(accepted, participants)

    ensure_output_dir(output_dir)
    write_analysis_summary(sessions, output_dir)
    write_analysis_report(sessions, output_dir)
    write_rejected_records(rejected, output_dir)

    print(f"Accepted rows: {len(accepted)}")
    print(f"Rejected rows: {len(rejected)}")
    print(f"Sessions processed: {len(sessions)}")
    print(f"Reports written to {output_dir}/:")
    print("- analysis_summary.csv")
    print("- analysis_report.txt")
    print("- rejected_records.txt")


if __name__ == "__main__":
    args = parse_args()
    try:
        run(args.profiles, args.sessions, args.output)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except PermissionError as e:
        print(f"Error: permission denied - {e}")
