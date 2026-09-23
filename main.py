from models import Session, SessionReport
from sample_data import SCENARIOS


def run_all_sessions():
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


if __name__ == "__main__":
    run_all_sessions()


    