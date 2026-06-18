import pandas as pd

# =====================
# 读取进攻数据
# =====================
attack = pd.read_csv(
    "data/ucl_squad_stats.csv",
    encoding="latin1"
)

# 清理球队名称
attack["Team"] = attack["Squad"].astype(str)

attack["Team"] = (
    attack["Team"]
    .str.replace("\xa0", " ", regex=False)
    .str.replace(r"^[a-z]{2}\s+", "", regex=True)
)

# =====================
# 读取合并后的数据
# =====================
combined = pd.read_csv(
    "data/combined_ucl_data.csv",
    encoding="latin1"
)

# 转数字
attack["Gls"] = pd.to_numeric(
    attack["Gls"],
    errors="coerce"
)

attack["Poss"] = pd.to_numeric(
    attack["Poss"],
    errors="coerce"
)

combined["GoalsConceded"] = pd.to_numeric(
    combined["GoalsConceded"],
    errors="coerce"
)

# =====================
# 合并
# =====================
df = attack.merge(
    combined[["Team", "GoalsConceded"]],
    on="Team",
    how="inner"
)

# =====================
# 冠军评分 V3
# =====================
df["PowerScore"] = (
    df["Gls"] * 2
    + df["Poss"] * 0.5
    - df["GoalsConceded"] * 1.5
)

# 排序
ranking = df.sort_values(
    "PowerScore",
    ascending=False
)

# 输出前15
print(
    ranking[
        [
            "Team",
            "Gls",
            "Poss",
            "GoalsConceded",
            "PowerScore"
        ]
    ].head(15)
)