import pandas as pd

df = pd.read_csv(
    "data/combined_ucl_data.csv",
    encoding="latin1"
)

df["GoalsScored"] = pd.to_numeric(df["GoalsScored"])
df["GoalsConceded"] = pd.to_numeric(df["GoalsConceded"])
df["Poss"] = pd.to_numeric(df["Poss"])

df["ChampionScore"] = (
    df["GoalsScored"] * 2
    + df["Poss"] * 0.5
    - df["GoalsConceded"] * 1.5
)

ranking = df.sort_values(
    "ChampionScore",
    ascending=False
)

print(
    ranking[
        [
            "Team",
            "GoalsScored",
            "Poss",
            "GoalsConceded",
            "ChampionScore"
        ]
    ]
)