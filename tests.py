from models import Observation, Participant, Session

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


if __name__ == "__main__": test_valid_observation_is_accepted() 
test_invalid_observation_is_rejected() 
test_participant_heart_rate_difference() 
test_resting_session_classifies_correctly() 
test_poor_quality_session_flagged_as_insufficient() 
print("\nAll tests passed.")