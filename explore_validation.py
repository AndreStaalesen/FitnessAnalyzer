from fitness_analyzer.loader import load_participants, load_sessions, build_sessions
from fitness_analyzer.report_writer import (
    ensure_output_dir,
    write_analysis_summary,
    write_analysis_report,
    write_rejected_records,
)

participants = load_participants("data/participants.csv")

accepted_valid, rejected_valid = load_sessions("data/fitness_sessions.csv", set(participants.keys()))
accepted_bad, rejected_bad = load_sessions("data/fitness_sessions_invalid.csv", set(participants.keys()))

all_accepted = accepted_valid + accepted_bad
all_rejected = rejected_valid + rejected_bad

sessions = build_sessions(all_accepted, participants)

ensure_output_dir("output")
write_analysis_summary(sessions, "output")
write_analysis_report(sessions, "output")
write_rejected_records(all_rejected, "output")

print(f"Processed {len(sessions)} sessions, {len(all_rejected)} rejected records.")
print("Output files written to the output/ folder.")
