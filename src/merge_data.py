import pandas as pd

# =========================
# 读取攻击数据
# =========================
attack = pd.read_csv(
    "data/ucl_squad_stats.csv",
    encoding="latin1"
)

# =========================
# 读取防守数据
# =========================
defense = pd.read_csv(
    "data/ucl_opponent_stats.csv.txt",
    sep="\t",
    encoding="latin1"
)

# =========================
# 创建球队名称列
# =========================
attack["Team"] = attack["Squad"].astype(str)
defense["Team"] = defense["Squad"].astype(str)

# =========================
# 清理攻击数据球队名
# 例如：
# eng Arsenal -> Arsenal
# es Barcelona -> Barcelona
# =========================
attack["Team"] = attack["Team"].str[3:]

# =========================
# 清理防守数据球队名
# =========================
defense["Team"] = defense["Team"].replace({
    "nl vs Ajax": "Ajax",
    "eng vs Arsenal": "Arsenal",
    "it vs Atalanta": "Atalanta",
    "es vs Athletic Club": "Athletic Club",
    "es vs AtlÃ©tico Madrid": "Atlético Madrid",
    "es vs Barcelona": "Barcelona",
    "de vs Bayern Munich": "Bayern Munich",
    "pt vs Benfica": "Benfica",
    "no vs BodÃ¸/Glimt": "Bodø/Glimt",
    "eng vs Chelsea": "Chelsea",
    "be vs Club Brugge": "Club Brugge",
    "de vs Dortmund": "Dortmund",
    "de vs Eintracht Frankfurt": "Eintracht Frankfurt",
    "dk vs FC Copenhagen": "FC Copenhagen",
    "kz vs FC Kairat": "FC Kairat",
    "tr vs Galatasaray": "Galatasaray",
    "it vs Inter": "Inter",
    "it vs Juventus": "Juventus",
    "de vs Leverkusen": "Leverkusen",
    "eng vs Liverpool": "Liverpool",
    "eng vs Manchester City": "Manchester City",
    "fr vs Marseille": "Marseille",
    "fr vs Monaco": "Monaco",
    "it vs Napoli": "Napoli",
    "eng vs Newcastle United": "Newcastle United",
    "gr vs Olympiacos": "Olympiacos",
    "cy vs Pafos FC": "Pafos FC",
    "fr vs Paris Saint-Germain": "Paris Saint-Germain",
    "nl vs PSV": "PSV",
    "az vs QarabaÄŸ": "Qarabağ",
    "es vs Real Madrid": "Real Madrid",
    "cz vs Slavia Prague": "Slavia Prague",
    "pt vs Sporting CP": "Sporting CP",
    "eng vs Tottenham Hotspur": "Tottenham Hotspur",
    "be vs Union SG": "Union SG",
    "es vs Villarreal": "Villarreal"
})

# =========================
# 查看是否匹配成功
# =========================
print("ATTACK")
print(attack["Team"].head(10))

print("\nDEFENSE")
print(defense["Team"].head(10))

# =========================
# 合并数据
# =========================
combined = pd.merge(
    attack,
    defense[["Team", "Gls"]],
    on="Team",
    how="inner"
)

# 重命名列
combined = combined.rename(columns={
    "Gls_x": "GoalsScored",
    "Gls_y": "GoalsConceded"
})

print("\n合并成功！")
print(combined[["Team", "GoalsScored", "GoalsConceded"]].head())

# 保存
combined.to_csv(
    "data/combined_ucl_data.csv",
    index=False
)

print("\n文件已保存：data/combined_ucl_data.csv")