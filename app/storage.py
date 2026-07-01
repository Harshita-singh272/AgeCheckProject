import json
from pathlib import Path

LOG_FILE = Path("data/activity_log.jsonl")


def save_verification_log(log_data):
    """
    Saves one verification record to activity_log.jsonl
    """
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        json.dump(log_data, file)
        file.write("\n")


def load_verification_logs():
    """
    Loads all verification records from activity_log.jsonl
    """
    logs = []

    if not LOG_FILE.exists():
        return logs

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line:
                logs.append(json.loads(line))

    return logs


def get_statistics():
    """
    Calculates verification statistics.
    """

    logs = load_verification_logs()

    stats = {
        "total_verifications": len(logs),
        "pass_count": 0,
        "fail_count": 0,
        "inconclusive_count": 0
    }

    for log in logs:

        decision = log.get("decision", "").upper()

        if decision == "PASS":
            stats["pass_count"] += 1

        elif decision == "FAIL":
            stats["fail_count"] += 1

        elif decision == "INCONCLUSIVE":
            stats["inconclusive_count"] += 1

    return stats

def get_heatmap_data():
    """
    Groups verification results by threshold.
    """

    logs = load_verification_logs()

    heatmap = {}

    for log in logs:

        threshold = str(log.get("threshold"))

        decision = log.get("decision", "").upper()

        if threshold not in heatmap:
            heatmap[threshold] = {
                "PASS": 0,
                "FAIL": 0,
                "INCONCLUSIVE": 0
            }

        if decision in heatmap[threshold]:
            heatmap[threshold][decision] += 1

    return heatmap
if __name__ == "__main__":

    print("\nStatistics:")
    print(get_statistics())

    print("\nHeatmap Data:")
    print(get_heatmap_data())