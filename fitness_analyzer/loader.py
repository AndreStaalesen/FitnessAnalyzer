import csv

from fitness_analyzer.models import Participant, Observation, Session
from fitness_analyzer.validation import (
    validate_participant_id,
    validate_session_record,
    InvalidIdentifierError,
    InvalidRecordError,
)


def load_participants(path):
    participants = {}
    try:
        with open(path, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                participant_id = validate_participant_id(row["participant_id"])
                participants[participant_id] = Participant(
                    participant_id=participant_id,
                    baseline_heart_rate=int(row["baseline_heart_rate"]),
                    baseline_skin_response=float(row["baseline_skin_response"]),
                    baseline_temperature=float(row["baseline_temperature"]),
                )
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find participants file: {path}")
    except csv.Error as e:
        raise InvalidRecordError(f"CSV formatting error in {path}: {e}")
    return participants

def load_sessions(path, known_participant_ids):
    accepted = []
    rejected = []
    try:
        with open(path, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row_number, row in enumerate(reader, start=1):
                try:
                    record = validate_session_record(row, row_number, path, known_participant_ids)
                    accepted.append(record)
                except (InvalidIdentifierError, InvalidRecordError) as e:
                    rejected.append(str(e))
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find sessions file: {path}")
    except csv.Error as e:
        raise InvalidRecordError(f"CSV formatting error in {path}: {e}")
    return accepted, rejected

def build_sessions(accepted_records, participants):
    sessions_by_id = {}
    for record in accepted_records:
        session_id = record["session_id"]
        if session_id not in sessions_by_id:
            sessions_by_id[session_id] = {
                "participant_id": record["participant_id"],
                "observations": [],
            }
        observation = Observation(
            timestamp=record["timestamp"],
            heart_rate=record["heart_rate"],
            skin_response=record["skin_response"],
            temperature=record["temperature"],
            activity_level=record["activity_level"],
            signal_quality=record["signal_quality"],
        )
        sessions_by_id[session_id]["observations"].append(observation)

    sessions = []
    for session_id, data in sessions_by_id.items():
        try:
            participant = participants[data["participant_id"]]
        except KeyError:
            raise InvalidRecordError(
                f"Session {session_id} references participant {data['participant_id']}, which was not loaded"
            )
        sessions.append(Session(participant, data["observations"], session_id=session_id))
    return sessions
