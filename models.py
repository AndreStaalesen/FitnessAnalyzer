class Observation: #This class is used to represent a single observation, while also checking the validity of the observation. It also provides properties to access the attributes of the observation.
    def __init__(self, timestamp, heart_rate, skin_response, temperature, activity_level, signal_quality):
        self.timestamp = timestamp
        self._heart_rate = heart_rate
        self._skin_response = skin_response
        self._temperature = temperature
        self._activity_level = activity_level
        self._signal_quality = signal_quality

    def is_valid(self):
        if self._heart_rate is None or self._skin_response is None:
            return False
        if not (30 <= self._heart_rate <= 220):
            return False
        if self._activity_level < 0 or self._activity_level > 1:
            return False
        if self._signal_quality < 0.5:
            return False
        return True

    @property
    def heart_rate(self):
        return self._heart_rate

    @property
    def skin_response(self):
        return self._skin_response

    @property
    def temperature(self):
        return self._temperature

    @property
    def activity_level(self):
        return self._activity_level

    @property
    def signal_quality(self):
        return self._signal_quality


class Participant: 
    def __init__(self, participant_id, baseline_heart_rate, baseline_skin_response, baseline_temperature):
        self.participant_id = participant_id
        self._baseline_heart_rate = baseline_heart_rate
        self._baseline_skin_response = baseline_skin_response
        self._baseline_temperature = baseline_temperature

    @property
    def baseline_heart_rate(self):
        return self._baseline_heart_rate

    @property
    def baseline_skin_response(self):
        return self._baseline_skin_response

    @property
    def baseline_temperature(self):
        return self._baseline_temperature

    def heart_rate_difference(self, observed_heart_rate):
        return observed_heart_rate - self._baseline_heart_rate

    