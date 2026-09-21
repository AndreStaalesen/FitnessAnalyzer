
from data_generator import generate_fitness_data 
profile, observations = generate_fitness_data( participant_id="P001", scenario="resting", seed=1, number_of_windows=8, ) 
print("PROFILE:") 
print(profile) 
print("\nOBSERVATIONS:") 
for obs in observations: print(obs)


from models import Observation
test_obs = Observation(**observations[0])
print("\nFirst observation valid?", test_obs.is_valid())
print("Heart rate via property:", test_obs.heart_rate)
print("Skin response via property:", test_obs.skin_response)




from models import Participant 
test_participant = Participant(**profile) 
print("\nBaseline HR:", test_participant.baseline_heart_rate) 
print("Difference for first observation:", test_participant.heart_rate_difference(observations[0]["heart_rate"]))


