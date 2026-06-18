import pandas as pd

df = pd.read_csv(
    "data/combined_ucl_data.csv",
    encoding="latin1"
)

df["GoalDifference"] = (
    df["GoalsScored"]
    - df["GoalsConceded"]
)

result = df.sort_values(
    "GoalDifference",
    ascending=False
)

print(
    result[
        [
            "Team",
            "GoalsScored",
            "GoalsConceded",
            "GoalDifference"
        ]
    ]
)