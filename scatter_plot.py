import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "data/ucl_squad_stats.csv",
    encoding="latin1"
)

df["Poss"] = pd.to_numeric(df["Poss"], errors="coerce")
df["Gls"] = pd.to_numeric(df["Gls"], errors="coerce")

plt.figure(figsize=(8,6))

plt.scatter(df["Poss"], df["Gls"])

plt.xlabel("Possession %")
plt.ylabel("Goals Scored")
plt.title("Possession vs Goals")

plt.grid(True)

plt.show()