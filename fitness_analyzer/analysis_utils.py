def format_percentage(count, total): 
    if total == 0: return "0%" 
    return f"{round((count / total) * 100, 1)}%"

def describe_classification(label): 
    descriptions = { 
        "resting": "Heart rate and activity stayed close to personal baseline.", 
        "moderate_activity": "Moderate elevation in heart rate and activity above baseline.", 
        "high_activity": "Significant elevation in heart rate and activity above baseline.", 
        "recovering": "Heart rate and activity declined notably during the session, trending back toward baseline.", 
        "insufficient_data": "Too few valid observations were available to classify this session reliably.", 
    } 
    return descriptions.get(label, "Unknown classification.")

def print_divider(character="=", length=40): print(character * length)

def summarize_sessions(session_dicts): 
    total_sessions = len(session_dicts) 
    classifications = [s["classification"] for s in session_dicts] 
    usable_sessions = [s for s in session_dicts if s["classification"] != "insufficient_data"] 
    return { "total_sessions": total_sessions, "usable_sessions": len(usable_sessions), "classification_counts": {label: classifications.count(label) for label in set(classifications)}, }


