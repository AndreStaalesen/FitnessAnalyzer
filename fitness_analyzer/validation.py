import re


class InvalidIdentifierError(ValueError):
    """Raised when an identifier has an invalid format."""


class InvalidRecordError(ValueError):
    """Raised when a CSV record cannot be accepted."""



PARTICIPANT_ID_PATTERN = r"^P\d{3}$"
SESSION_ID_PATTERN = r"^FIT-\d{4}-\d{3}$"


def validate_participant_id(participant_id):
    if not re.fullmatch(PARTICIPANT_ID_PATTERN, participant_id):
        raise InvalidIdentifierError(f"'{participant_id}' is not a valid participant ID (expected format: P001)")
    return participant_id


def validate_session_id(session_id):
    if not re.fullmatch(SESSION_ID_PATTERN, session_id):
        raise InvalidIdentifierError(f"'{session_id}' is not a valid session ID (expected format: FIT-2026-001)")
    return session_id

