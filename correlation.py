import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "data/combined_ucl_data.csv",
    encoding="latin1"
)

corr = df["Poss"].corr(df["GoalsScored"])

print("Correlation =", round(corr, 3))

plt.scatter(
    df["Poss"],
    df["GoalsScored"]
)

plt.xlabel("Possession %")
plt.ylabel("Goals Scored")
plt.title("Possession vs Goals")

plt.grid(True)

plt.show()