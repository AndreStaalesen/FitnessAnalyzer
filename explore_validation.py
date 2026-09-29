from fitness_analyzer.loader import load_participants, load_sessions, build_sessions

participants = load_participants("data/participants.csv")
print(f"Loaded {len(participants)} participants")

accepted, rejected = load_sessions("data/fitness_sessions.csv", set(participants.keys()))
print(f"\nfitness_sessions.csv: {len(accepted)} accepted, {len(rejected)} rejected")

accepted_bad, rejected_bad = load_sessions("data/fitness_sessions_invalid.csv", set(participants.keys()))
print(f"fitness_sessions_invalid.csv: {len(accepted_bad)} accepted, {len(rejected_bad)} rejected")
print("\nRejected rows from the invalid file:")
for reason in rejected_bad:
    print(" -", reason)

sessions = build_sessions(accepted, participants)
print(f"\nBuilt {len(sessions)} sessions from the valid file")
for session in sessions:
    print(f"{session.participant.participant_id}: {session.classify()} ({session.valid_observation_count}/{session.total_observations} valid)")