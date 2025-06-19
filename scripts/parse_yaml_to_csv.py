import os
import yaml
import pandas as pd
from glob import glob

RAW_DATA_DIR = "data/raw/"
OUTPUT_CSV = "data/match_data.csv"

def parse_match(file_path):
    with open(file_path, 'r') as f:
        match = yaml.safe_load(f)

    info = match.get("info", {})
    teams = info.get("teams", [])
    venue = info.get("venue", "")
    toss_winner = info.get("toss", {}).get("winner", "")
    toss_decision = info.get("toss", {}).get("decision", "")
    winner = info.get("outcome", {}).get("winner", "")
    result_type = info.get("outcome", {}).get("result", "")
    date = "-".join(map(str, info.get("dates", [None])))

    innings = match.get("innings", [])
    if len(innings) < 2:
        return None

    performance = {team: {"runs": 0, "wickets": 0, "overs": 0} for team in teams}

    for inning in innings:
        inning_data = list(inning.values())[0]
        team_name = inning_data.get("team")
        deliveries = inning_data.get("deliveries", [])
        runs, wickets = 0, 0
        overs_set = set()
        for d in deliveries:
            ball = list(d.keys())[0]
            delivery = d[ball]
            runs += delivery.get("runs", {}).get("total", 0)
            if "wicket" in delivery:
                wickets += 1
            overs_set.add(int(float(ball)))

        if team_name in performance:
            performance[team_name]["runs"] = runs
            performance[team_name]["wickets"] = wickets
            performance[team_name]["overs"] = len(overs_set)

    row = {
        "date": date,
        "venue": venue,
        "team1": teams[0],
        "team2": teams[1],
        "team1_runs": performance[teams[0]]['runs'],
        "team2_runs": performance[teams[1]]['runs'],
        "team1_wickets": performance[teams[0]]['wickets'],
        "team2_wickets": performance[teams[1]]['wickets'],
        "team1_overs": performance[teams[0]]['overs'],
        "team2_overs": performance[teams[1]]['overs'],
        "toss_winner": toss_winner,
        "toss_decision": toss_decision,
        "match_winner": winner,
        "result_type": result_type
    }

    return row

def build_dataset():
    print("📦 Parsing YAML files to CSV...")
    all_files = glob(os.path.join(RAW_DATA_DIR, "*.yaml"))
    data = []

    for file in all_files:
        parsed = parse_match(file)
        if parsed:
            data.append(parsed)

    df = pd.DataFrame(data)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/match_data.csv", index=False)
    print(f"✅ Created dataset with {len(df)} matches → data/match_data.csv")

if __name__ == "__main__":
    build_dataset()
