# A - Smart Fitness Session Analyzer ACIT4420 - Problem Solving with Scripting - Andre Staalesen, Student Number: 404337, https://github.com/AndreStaalesen/FitnessAnalyzer
## Description 
This program simulates a fitness centers wearable-device data pipeline. It takes raw participant and observation data from the provided generator file, validates it, compares it against each participant's personal baseline, classifies the overall session, and prints a console report. Five scenarios are included, covering normal, unusual, and invalid-data cases.  

## Repository structure 
This project repository is split into additional modules for readability: “main.py” runs all five sample sessions and prints their reports. “models.py” contains all the classes. "sample_data.py" contains five scenario configurations. "analysis_utils.py" contains standalone functions for formatting, description text, and cross-session summarizing. "tests.py" runs automated checks for validation, comparison, and classification logic. "requirements.txt" states that no external packages are required. The files from the provided data generator folder are also included.

## Class design 
“Observation” represents a single measurement window, stores its values as private attributes, exposed through read-only properties, and owns “is_valid()”, which rejects an observation if it has missing values, an impossible heart rate, an out-of-range activity level, or unreliable signal quality. “Participant” represents a person and their personal baseline. It provides “heart_rate_difference()”, “skin_response_difference()”, and “temperature_difference()”, which compare an observed value against that person's own baseline rather than a fixed threshold. “Session” represents one full session for one participant. This is the clearest example of composition in my project. One “Session” has one participant and has a list of Observation objects. It filters out invalid observations, computes averages, minimums, and maximums, compares averages against the participant's baseline, detects a recovery pattern by comparing the first and second half of the session, classifies the session overall, and packages the full result as a dictionary via “to_dict()”. It also provides “from_generator()” which is a classmethod that builds a complete “Session” directly from the data generator in a single call, acting as an alternate constructor. “SessionReport” takes a finished “Session” and turns its results into a readable console report. Kept separate from "Session” deliberately, “Session” is responsible for analysis, while “SessionReport” is responsible for presentation, so a different report format could be added later without touching any analysis logic. 

## Composition, encapsulation, and inheritance
“Session” is composed of a “Participant” and a list of “Observation”.
All measurement and baseline values are stored as private attributes and exposed only through properties or methods, rather than being modified directly from outside their class.
This project does not use inheritance. A “Session” is not a specialised kind of “Observation” or “Participant”, rather its built out of them, so an inheritance relationship would be artificial here. I feel composition is a better fit for this problem. 

## Assumptions and classification rules
A session needs at least 4 valid observations to be classified, and fewer than that returns “insufficient_data”. Recovery is detected by comparing the first half of a session's valid observations against the second half. If heart rate drops by more than 15 bpm, activity drops by more than 0.15, and heart rate is still more than 10 bpm above baseline by the second half, the session is classified as “recovering”. These thresholds were deliberately set higher than the generator's typical random noise, after testing showed lower thresholds produced false positives on scenarios with no real trend. If a session isn't recovering, it's classified using how far the average heart rate sits above the participant's personal baseline, combined with average activity level. Under roughly 10 bpm above baseline and low activity is “resting”, under 35 bpm above baseline and moderate activity is “moderate_activity”, anything higher is “high_activity". An observation is considered invalid if its heart rate or skin response is missing, its heart rate falls outside 30–220 bpm, its activity level is outside 0–1, or its signal quality is below 0.5. 

## Installation and running 
This project uses only the Python standard library.
git clone https://github.com/AndreStaalesen/FitnessAnalyzer
cd FitnessAnalyzer
python main.py 
To run the automated tests: python tests.py 

## Example output 
Resting session ======================================== Session Report for P001 ======================================== Observations used: 10/10 Average Heart Rate: 64.1 Average Activity Level: 0.14 Heart rate range: 60 - 67 Activity level range: 0.05 - 0.2 Avg skin response vs baseline: -0.02 Avg temperature vs baseline: -0.05 Classification: resting ======================================== Heart rate and activity stayed close to personal baseline. Data quality: 100.0% usable. A full output includes five such reports for all scenarios, followed by an overall summary across all sessions.

## Known limitations
Classification thresholds like bpm and activity cutoffs were tuned by testing against the five sample scenarios rather than derived from clinical data. Some cases near a threshold boundary could be classified differently than a human might judge them.
The recovery check only compares the first half of a session against the second half. A session with a more complex pattern would not be detected accurately. The ”poor_quality” scenario, with the seed used in “sample_data.py”, happens to invalidate all 12 observations, resulting in “insufficient_data” rather than a partially valid session. other seeds would show a mix of valid and invalid observations instead. 
