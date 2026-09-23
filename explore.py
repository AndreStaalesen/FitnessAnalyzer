
from data_generator import generate_fitness_data 
profile, observations = generate_fitness_data( participant_id="P001", scenario="resting", seed=1, number_of_windows=8, ) 
print("PROFILE:") 
print(profile) 
print("\nOBSERVATIONS:") 
for obs in observations: print(obs)


from models import Observation
test_obs = Observation(**observations[0])





from models import Participant 
test_participant = Participant(**profile) 




from models import Session
quick_session = Session.from_generator("P001", "recovery", seed=7, number_of_windows=12) 
print("\nClassification:", quick_session.classify()) 
print("Valid:", quick_session.valid_observation_count, "/", quick_session.total_observations) 
print("Avg HR:", quick_session.average_heart_rate(), " Avg activity:", quick_session.average_activity_level())



from models import SessionReport 
report = SessionReport(quick_session) 
report.print_report()






print("\nAs a dict:") 
print(quick_session.to_dict())