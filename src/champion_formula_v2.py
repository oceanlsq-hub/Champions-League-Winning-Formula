import pandas as pd

df = pd.read_csv("data/combined_ucl_data.csv")

# 数字转换
df["GoalsScored"] = pd.to_numeric(df["GoalsScored"])
df["GoalsConceded"] = pd.to_numeric(df["GoalsConceded"])

# 攻守差
df["GoalDifference"] = (
    df["GoalsScored"]
    - df["GoalsConceded"]
)

ranking = df.sort_values(
    "GoalDifference",
    ascending=False
)

print(
    ranking[
        [
            "Team",
            "GoalsScored",
            "GoalsConceded",
            "GoalDifference"
        ]
    ].head(15)
)