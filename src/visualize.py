import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/combined_ucl_data.csv")

df["ChampionScore"] = (
    df["GoalsScored"] * 1.5
    + df["Poss"] * 0.5
    - df["GoalsConceded"] * 1.2
)

df = df.sort_values(
    by="ChampionScore",
    ascending=False
).head(10)

plt.figure(figsize=(10,6))

plt.barh(
    df["Team"],
    df["ChampionScore"]
)

plt.xlabel("Champion Score")
plt.title("Top UCL Title Contenders")

plt.gca().invert_yaxis()

plt.tight_layout()

plt.savefig("ucl_prediction.png")