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



def _require_field(row, field, row_number, source_file):
    value = row.get(field)
    if value is None or value == "":
        raise InvalidRecordError(
            f"{source_file}, row {row_number}: missing required field '{field}'"
        )
    return value


def _parse_number(value, field, row_number, source_file, as_type):
    try:
        return as_type(value)
    except ValueError:
        raise InvalidRecordError(
            f"{source_file}, row {row_number}: field '{field}' has value '{value}', which cannot be converted to a number"
        )



def validate_session_record(row, row_number, source_file, known_participant_ids):
    if None in row:
        raise InvalidRecordError(
            f"{source_file}, row {row_number}: row has more fields than expected"
        )
    try:
        session_id = validate_session_id(row.get("session_id", ""))
    except InvalidIdentifierError as e:
        raise InvalidIdentifierError(f"{source_file}, row {row_number}, field 'session_id': {e}")

    try:
        participant_id = validate_participant_id(row.get("participant_id", ""))
    except InvalidIdentifierError as e:
        raise InvalidIdentifierError(f"{source_file}, row {row_number}, field 'participant_id': {e}")

    if participant_id not in known_participant_ids:
        raise InvalidRecordError(
            f"{source_file}, row {row_number}: participant '{participant_id}' does not exist in participants.csv"
        )

    for field in ["timestamp", "heart_rate", "skin_response", "temperature", "activity_level", "signal_quality"]:
        _require_field(row, field, row_number, source_file)

    timestamp = _parse_number(row["timestamp"], "timestamp", row_number, source_file, int)
    heart_rate = _parse_number(row["heart_rate"], "heart_rate", row_number, source_file, int)
    skin_response = _parse_number(row["skin_response"], "skin_response", row_number, source_file, float)
    temperature = _parse_number(row["temperature"], "temperature", row_number, source_file, float)
    activity_level = _parse_number(row["activity_level"], "activity_level", row_number, source_file, float)
    signal_quality = _parse_number(row["signal_quality"], "signal_quality", row_number, source_file, float)

    if not (30 <= heart_rate <= 220):
        raise InvalidRecordError(f"{source_file}, row {row_number}: heart_rate {heart_rate} is out of range (30-220)")
    if not (0 <= activity_level <= 1):
        raise InvalidRecordError(f"{source_file}, row {row_number}: activity_level {activity_level} is out of range (0-1)")
    if not (0 <= signal_quality <= 1):
        raise InvalidRecordError(f"{source_file}, row {row_number}: signal_quality {signal_quality} is out of range (0-1)")
    if not (25 <= temperature <= 42):
        raise InvalidRecordError(f"{source_file}, row {row_number}: temperature {temperature} is out of range (25-42)")
    if skin_response < 0:
        raise InvalidRecordError(f"{source_file}, row {row_number}: skin_response {skin_response} cannot be negative")

    return {
        "session_id": session_id,
        "participant_id": participant_id,
        "timestamp": timestamp,
        "heart_rate": heart_rate,
        "skin_response": skin_response,
        "temperature": temperature,
        "activity_level": activity_level,
        "signal_quality": signal_quality,
    }

