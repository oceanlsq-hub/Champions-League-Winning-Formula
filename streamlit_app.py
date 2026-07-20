import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="UCL Winning Formula", layout="wide")
st.title("📊 UCL Winning Formula")
st.markdown("A data-driven analysis of what makes a Champions League winner.")

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CHART_DIR = os.path.join(os.path.dirname(__file__), "charts")

@st.cache_data
def load_data():
    attack = pd.read_csv(os.path.join(DATA_DIR, "ucl_squad_stats.csv"), encoding="latin1")
    defense = pd.read_csv(os.path.join(DATA_DIR, "ucl_opponent_stats.csv.txt"), sep="\t")
    combined = pd.read_csv(os.path.join(DATA_DIR, "combined_ucl_data.csv"), encoding="latin1")

    attack["Team"] = attack["Squad"].str.replace(r"^[a-z]{2}\s", "", regex=True)
    defense["Team"] = defense["Squad"].str.replace(r"^[a-z]{2}\svs\s", "", regex=True)

    attack["GF"] = pd.to_numeric(attack["Gls"], errors="coerce")
    attack["Poss"] = pd.to_numeric(attack["Poss"], errors="coerce")
    combined["GoalsScored"] = pd.to_numeric(combined["GoalsScored"], errors="coerce")
    combined["GoalsConceded"] = pd.to_numeric(combined["GoalsConceded"], errors="coerce")
    defense["GA"] = pd.to_numeric(defense["Gls"], errors="coerce")

    return attack, defense, combined

attack, defense, combined = load_data()

df = attack[["Team", "GF", "Poss"]].merge(combined[["Team", "GoalsScored", "GoalsConceded"]], on="Team")
df["GD"] = df["GoalsScored"] - df["GoalsConceded"]

st.subheader("Raw Data Preview")
tab1, tab2, tab3 = st.tabs(["Attack Stats", "Defense Stats", "Combined"])
with tab1: st.dataframe(attack.head(10), use_container_width=True)
with tab2: st.dataframe(defense.head(10), use_container_width=True)
with tab3: st.dataframe(combined.head(10), use_container_width=True)

st.subheader("Goal Difference Ranking")
ranking = df.sort_values("GD", ascending=False)
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(ranking["Team"], ranking["GD"], color="mediumseagreen")
ax.axvline(0, color="gray", linewidth=0.5)
ax.set_xlabel("Goal Difference")
ax.set_title("Teams Ranked by Goal Difference")
ax.invert_yaxis()
st.pyplot(fig)
plt.close()

st.dataframe(ranking[["Team", "GoalsScored", "GoalsConceded", "GD"]].reset_index(drop=True))

st.subheader("Correlation: Goals & Possession")
heat_df = attack[["Team", "GF", "Poss"]].merge(defense[["Team", "GA"]], on="Team")
corr_data = heat_df[["GF", "GA", "Poss"]].rename(columns={"GF": "GF (Scored)", "GA": "GA (Conceded)"})
fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(corr_data.corr(), annot=True, fmt=".2f", cmap="coolwarm",
            vmin=-1, vmax=1, square=True, linewidths=1, ax=ax,
            annot_kws={"fontsize": 12})
ax.set_title("Correlation Heatmap")
st.pyplot(fig)
plt.close()

st.subheader("Possession vs Goals Scored")
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(df["Poss"], df["GF"], alpha=0.7, s=100, color="purple", edgecolors="white")
for _, row in df.iterrows():
    ax.annotate(row["Team"], (row["Poss"], row["GF"]), fontsize=8, ha="center", va="bottom")
ax.set_xlabel("Possession (%)")
ax.set_ylabel("Goals Scored")
ax.set_title("Possession vs Goals Scored")
ax.grid(True, alpha=0.3)
corr = df["Poss"].corr(df["GF"])
ax.text(0.05, 0.95, f"r = {corr:.2f}", transform=ax.transAxes, fontsize=12,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))
st.pyplot(fig)
plt.close()

st.subheader("Winning Formula Comparison")
col1, col2 = st.columns(2)

models = {
    "Balanced (GF×0.4, GA×0.4, GD×0.2)": (0.4, 0.4, 0.2),
    "Attack-heavy (GF×0.5, GA×0.3, GD×0.2)": (0.5, 0.3, 0.2),
    "Defence-first (GF×0.3, GA×0.5, GD×0.2)": (0.3, 0.5, 0.2),
}

with col1:
    selected = st.selectbox("Select weight model", list(models.keys()))
    w_gf, w_ga, w_gd = models[selected]
    df["Score"] = df["GF"] * w_gf - df["GA"] * w_ga + df["GD"] * w_gd
    result = df.sort_values("Score", ascending=False)[["Team", "GF", "GA", "GD", "Score"]].reset_index(drop=True)
    result.index = result.index + 1
    st.dataframe(result.head(10), use_container_width=True)

with col2:
    fig, ax = plt.subplots(figsize=(8, 4))
    top5 = result.head(5)
    colors = plt.cm.Set2(np.linspace(0, 1, 5))
    ax.barh(top5["Team"], top5["Score"], color=colors)
    ax.set_xlabel("Winning Score")
    ax.set_title(f"Top 5 Teams ({selected.split('(')[0].strip()})")
    ax.invert_yaxis()
    for i, v in enumerate(top5["Score"]):
        ax.text(v + 0.1, i, f"{v:.1f}", va="center")
    st.pyplot(fig)
    plt.close()

st.subheader("Model Comparison")
all_results = {}
for name, (w1, w2, w3) in models.items():
    df["Score"] = df["GF"] * w1 - df["GA"] * w2 + df["GD"] * w3
    all_results[name] = df.sort_values("Score", ascending=False)["Team"].head(8).tolist()

comparison = pd.DataFrame(all_results)
comparison.index = [f"#{i+1}" for i in range(8)]
st.dataframe(comparison, use_container_width=True)

actual_top8 = {"Liverpool", "Barcelona", "Arsenal", "Inter",
               "Atletico Madrid", "Bayer Leverkusen", "Lille", "Aston Villa"}
st.write("**Match with actual 2024-25 Round of 16 qualifiers:**")
for name, teams in all_results.items():
    match = len(set(teams) & actual_top8)
    short = name.split("(")[0].strip()
    st.write(f"• {short}: {match}/8 teams match")

st.markdown("---")
st.caption("Data: FBref 2024-25 UCL | Code: [GitHub](https://github.com/oceanlsq-hub/Champions-League-Winning-Formula)")
