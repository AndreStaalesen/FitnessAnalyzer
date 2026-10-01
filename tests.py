from fitness_analyzer.models import Observation, Participant, Session
from fitness_analyzer.validation import (
    validate_participant_id,
    validate_session_id,
    validate_session_record,
    InvalidIdentifierError,
    InvalidRecordError,
)
from fitness_analyzer.loader import load_participants, load_sessions

def test_valid_observation_is_accepted(): 
    obs = Observation(timestamp=0, heart_rate=70, 
    skin_response=1.5, temperature=32.0, activity_level=0.3, signal_quality=0.9) 
    assert obs.is_valid() is True 
    print("PASS: valid observation accepted")

def test_invalid_observation_is_rejected(): 
    missing_hr = Observation(timestamp=0, heart_rate=None, skin_response=1.5, temperature=32.0, activity_level=0.3, signal_quality=0.9) 
    impossible_hr = Observation(timestamp=1, heart_rate=300, skin_response=1.5, temperature=32.0, activity_level=0.3, signal_quality=0.9) 
    bad_activity = Observation(timestamp=2, heart_rate=70, skin_response=1.5, temperature=32.0, activity_level=-0.2, signal_quality=0.9) 
    low_signal = Observation(timestamp=3, heart_rate=70, skin_response=1.5, temperature=32.0, activity_level=0.3, signal_quality=0.1) 
    assert missing_hr.is_valid() is False 
    assert impossible_hr.is_valid() is False 
    assert bad_activity.is_valid() is False 
    assert low_signal.is_valid() is False 
    print("PASS: invalid observations rejected")

def test_participant_heart_rate_difference(): 
    participant = Participant(participant_id="TEST", baseline_heart_rate=60, baseline_skin_response=1.5, baseline_temperature=32.0) 
    assert participant.heart_rate_difference(75) == 15 
    assert participant.heart_rate_difference(60) == 0 
    assert participant.heart_rate_difference(50) == -10 
    print("PASS: heart rate difference calculated correctly")


def test_resting_session_classifies_correctly(): 
    session = Session.from_generator("TEST", "resting", seed=1, number_of_windows=10) 
    assert session.classify() == "resting" 
    print("PASS: resting scenario classified correctly") 

def test_poor_quality_session_flagged_as_insufficient(): 
    session = Session.from_generator("TEST", "poor_quality", seed=1, number_of_windows=12) 
    assert session.valid_observation_count < session.total_observations 
    print("PASS: poor quality scenario has invalid observations filtered out")

def test_valid_participant_id_accepted():
    assert validate_participant_id("P001") == "P001"
    print("PASS: valid participant ID accepted")


def test_invalid_participant_id_rejected():
    try:
        validate_participant_id("001")
        assert False, "Expected InvalidIdentifierError to be raised"
    except InvalidIdentifierError:
        print("PASS: invalid participant ID rejected")


def test_invalid_session_id_rejected():
    try:
        validate_session_id("FIT-26-102")
        assert False, "Expected InvalidIdentifierError to be raised"
    except InvalidIdentifierError:
        print("PASS: invalid session ID rejected")


def test_session_record_rejects_bad_heart_rate():
    row = {
        "session_id": "FIT-2026-999", "participant_id": "P001", "timestamp": "0",
        "heart_rate": "fast", "skin_response": "1.0", "temperature": "32.0",
        "activity_level": "0.1", "signal_quality": "0.9",
    }
    try:
        validate_session_record(row, 1, "test.csv", {"P001"})
        assert False, "Expected InvalidRecordError to be raised"
    except InvalidRecordError:
        print("PASS: unconvertible heart rate value rejected")


def test_load_participants_from_real_file():
    participants = load_participants("data/participants.csv")
    assert len(participants) == 3
    assert "P001" in participants
    print("PASS: participants loaded correctly from participants.csv")


def test_load_sessions_counts_match_expected():
    participants = load_participants("data/participants.csv")
    known_ids = set(participants.keys())
    accepted, rejected = load_sessions("data/fitness_sessions_invalid.csv", known_ids)
    assert len(accepted) == 1
    assert len(rejected) == 10
    print("PASS: fitness_sessions_invalid.csv produces expected accepted/rejected counts")


def test_missing_file_raises_file_not_found():
    try:
        load_participants("data/does_not_exist.csv")
        assert False, "Expected FileNotFoundError to be raised"
    except FileNotFoundError:
        print("PASS: missing file correctly raises FileNotFoundError")

if __name__ == "__main__":
    test_valid_observation_is_accepted()
    test_invalid_observation_is_rejected()
    test_participant_heart_rate_difference()
    test_resting_session_classifies_correctly()
    test_poor_quality_session_flagged_as_insufficient()
    test_valid_participant_id_accepted()
    test_invalid_participant_id_rejected()
    test_invalid_session_id_rejected()
    test_session_record_rejects_bad_heart_rate()
    test_load_participants_from_real_file()
    test_load_sessions_counts_match_expected()
    test_missing_file_raises_file_not_found()
    print("\nAll tests passed.")
    