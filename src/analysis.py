import pandas as pd

# 读取进攻数据
attack = pd.read_csv(
    "data/ucl_squad_stats.csv",
    encoding="latin1"
)

# 读取防守数据
defense = pd.read_csv(
    "data/ucl_opponent_stats.csv.txt",
    sep="\t"
)

# 提取球队名
attack["Team"] = attack["Squad"].str.replace(
    r"^[a-z]{2}\s",
    "",
    regex=True
)

defense["Team"] = defense["Squad"].str.replace(
    r"^[a-z]{2}\svs\s",
    "",
    regex=True
)

# 进球
attack["GF"] = pd.to_numeric(
    attack["Gls"],
    errors="coerce"
)

# 失球
defense["GA"] = pd.to_numeric(
    defense["Gls"],
    errors="coerce"
)

# 合并
combined = pd.merge(
    attack[["Team", "GF"]],
    defense[["Team", "GA"]],
    on="Team"
)

# 净胜球
combined["GD"] = combined["GF"] - combined["GA"]

# 排名
ranking = combined.sort_values(
    by="GD",
    ascending=False
)

print(ranking.head(15))
import matplotlib.pyplot as plt


top10 = ranking.head(10)


plt.figure(figsize=(10,6))

plt.bar(
    top10["Team"],
    top10["GD"]
)

plt.xticks(
    rotation=45
)

plt.title(
    "Champions League Winning Formula - Top 10 Goal Difference"
)

plt.ylabel(
    "Goal Difference"
)

plt.tight_layout()

plt.savefig(
    "charts/top10_goal_difference.png"
)

plt.show()
# Winning Formula Score

ranking["WinningScore"] = (
    ranking["GF"] * 0.4
    -
    ranking["GA"] * 0.4
    +
    ranking["GD"] * 0.2
)


final_rank = ranking.sort_values(
    by="WinningScore",
    ascending=False
)


print(final_rank.head(10))
import os

os.makedirs("results", exist_ok=True)

final_rank.to_csv(
    "results/winning_formula_ranking.csv",
    index=False
)

print("Saved successfully!")