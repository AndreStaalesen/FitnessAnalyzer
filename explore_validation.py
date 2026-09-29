from fitness_analyzer.validation import validate_participant_id, validate_session_id, InvalidIdentifierError

good_participant = "P001"
bad_participant = "001"
good_session = "FIT-2026-001"
bad_session = "FIT-26-102"

print(validate_participant_id(good_participant), "is valid")

try:
    validate_participant_id(bad_participant)
except InvalidIdentifierError as e:
    print("Caught error:", e)

print(validate_session_id(good_session), "is valid")

try:
    validate_session_id(bad_session)
except InvalidIdentifierError as e:
    print("Caught error:", e)
    