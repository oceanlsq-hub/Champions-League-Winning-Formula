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

# =========================
# 相关系数热力图
# =========================
print("\n=== Correlation Heatmap ===\n")

combined_corr = combined.copy()
combined_corr["Poss"] = attack["Poss"]  # add possession

plt.figure(figsize=(8, 6))
corr_matrix = combined_corr[["GF", "GA", "GD"]].corr()
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1,
            square=True, linewidths=1)
plt.title("Correlation: GF, GA, GD")
plt.tight_layout()
plt.savefig(os.path.join("..", "charts", "correlation_heatmap.png"))
plt.show()

# =========================
# Possession vs Goals 散点图
# =========================
print("\n=== Possession vs Goals Scored ===\n")
corr_poss = combined_corr["Poss"].corr(combined_corr["GF"])
print(f"Correlation between Possession and Goals Scored: {corr_poss:.3f}")

plt.figure(figsize=(10, 6))
plt.scatter(combined_corr["Poss"], combined_corr["GF"], alpha=0.7, s=80, color="purple")
for _, row in combined_corr.iterrows():
    plt.annotate(row["Team"], (row["Poss"], row["GF"]), fontsize=8, ha="center", va="bottom")
plt.xlabel("Possession (%)")
plt.ylabel("Goals Scored")
plt.title("Possession vs Goals Scored (2024-25 UCL)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join("..", "charts", "possession_vs_goals.png"))
plt.show()


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