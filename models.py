from data_generator import generate_fitness_data

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

    def skin_response_difference(self, observed_skin_response):
        return round(observed_skin_response - self._baseline_skin_response, 2)

    def temperature_difference(self, observed_temperature): 
        return round(observed_temperature - self._baseline_temperature, 2)

    
class Session:
    def __init__(self, participant, observations):
        self.participant = participant
        self._observations = observations

    @property
    def valid_observations(self):
        return [obs for obs in self._observations if obs.is_valid()]

    @property
    def total_observations(self):
        return len(self._observations)

    @property
    def valid_observation_count(self):
        return len(self.valid_observations)


    def average_heart_rate(self): 
        valid = self.valid_observations 
        if not valid: return None 
        total = sum(obs.heart_rate for obs in valid) 
        return round(total / len(valid), 2)

    def average_activity_level(self): 
        valid = self.valid_observations 
        if not valid: return None 
        total = sum(obs.activity_level for obs in valid) 
        return round(total / len(valid), 2)

    def average_skin_response_difference(self): 
        valid = self.valid_observations 
        if not valid: return None 
        total = sum(self.participant.skin_response_difference(obs.skin_response) for obs in valid) 
        return round(total / len(valid), 2) 

    def average_temperature_difference(self): 
        valid = self.valid_observations 
        if not valid: return None 
        total = sum(self.participant.temperature_difference(obs.temperature) for obs in valid) 
        return round(total / len(valid), 2)

    def min_heart_rate(self):
        valid = self.valid_observations 
        if not valid: return None 
        return min(obs.heart_rate for obs in valid) 

    def max_heart_rate(self):
        valid = self.valid_observations 
        if not valid: return None 
        return max(obs.heart_rate for obs in valid) 

    def min_activity_level(self):
        valid = self.valid_observations 
        if not valid: return None 
        return min(obs.activity_level for obs in valid) 

    def max_activity_level(self):
        valid = self.valid_observations 
        if not valid: return None 
        return max(obs.activity_level for obs in valid)

    def is_recovering(self): 
        valid = self.valid_observations 
        if len(valid) < 6: return False 
        midpoint = len(valid) // 2 
        first_half = valid[:midpoint] 
        second_half = valid[midpoint:] 
        first_avg_hr = sum(o.heart_rate for o in first_half) / len(first_half) 
        second_avg_hr = sum(o.heart_rate for o in second_half) / len(second_half) 
        first_avg_activity = sum(o.activity_level for o in first_half) / len(first_half) 
        second_avg_activity = sum(o.activity_level for o in second_half) / len(second_half) 
        hr_declining = second_avg_hr < first_avg_hr - 15 
        activity_declining = second_avg_activity < first_avg_activity - 0.15 
        still_elevated = self.participant.heart_rate_difference(second_avg_hr) > 10 
        return hr_declining and activity_declining and still_elevated


    def classify(self): 
        if self.valid_observation_count < 4:
            return "insufficient_data"
        if self.is_recovering():
            return "recovering" 
        avg_hr = self.average_heart_rate()
        avg_activity = self.average_activity_level()
        hr_diff = self.participant.heart_rate_difference(avg_hr)
        if hr_diff < 10 and avg_activity < 0.25:
            return "resting"
        elif hr_diff < 35 and avg_activity < 0.6:
            return "moderate_activity"
        else: 
            return "high_activity"

    def to_dict(self): 
        return {"participant_id": self.participant.participant_id, 
                "total_observations": self.total_observations, 
                "valid_observations": self.valid_observation_count, 
                "average_heart_rate": self.average_heart_rate(), 
                "min_heart_rate": self.min_heart_rate(), 
                "max_heart_rate": self.max_heart_rate(), 
                "average_activity_level": self.average_activity_level(), 
                "min_activity_level": self.min_activity_level(), 
                "max_activity_level": self.max_activity_level(), 
                "average_skin_response_difference": self.average_skin_response_difference(), 
                "average_temperature_difference": self.average_temperature_difference(), 
                "classification": self.classify(), }

    @classmethod
    def from_generator(cls, participant_id, scenario, seed=None, number_of_windows=12):
        from data_generator import generate_fitness_data
        profile, observations = generate_fitness_data(
            participant_id=participant_id,
            scenario=scenario,
            seed=seed,
            number_of_windows=number_of_windows,
        )
        participant = Participant(**profile)
        observation_objects = [Observation(**obs) for obs in observations]
        return cls(participant, observation_objects)


class SessionReport:
    def __init__(self, session):
        self.session = session

    def print_report(self):
        s = self.session 
        print("="*40) 
        print(f"Session Report for {s.participant.participant_id}") 
        print("="*40) 
        print(f"Observations used: {s.valid_observation_count}/{s.total_observations}")
        print(f"Average Heart Rate: {s.average_heart_rate()}")
        print(f"Average Activity Level: {s.average_activity_level()}")
        print(f"Heart rate range: {s.min_heart_rate()} - {s.max_heart_rate()}")
        print(f"Activity level range: {s.min_activity_level()} - {s.max_activity_level()}")
        print(f"Avg skin response vs baseline: {s.average_skin_response_difference()}")
        print(f"Avg temperature vs baseline: {s.average_temperature_difference()}")
        print(f"Classification: {s.classify()}")
        print("="*40)

