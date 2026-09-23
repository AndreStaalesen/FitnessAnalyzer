from models import Session, SessionReport 
from sample_data import SCENARIOS 
from analysis_utils import describe_classification, print_divider, summarize_sessions, format_percentage

def run_all_sessions(): 
    all_results = [] 
    for config in SCENARIOS: 
        print(f"\n{config['label']}") 
        session = Session.from_generator( 
            participant_id=config["participant_id"], 
            scenario=config["scenario"], 
            seed=config["seed"], 
            number_of_windows=config["number_of_windows"], 
        ) 
        report = SessionReport(session) 
        report.print_report() 
        print(describe_classification(session.classify())) 
        print("Data quality:", format_percentage(session.valid_observation_count, session.total_observations), "usable") 
        all_results.append(session.to_dict()) 

    print_divider("-", 40) 
    print("Overall summary across all sessions:") 
    print(summarize_sessions(all_results))

if __name__ == "__main__":
    run_all_sessions()
