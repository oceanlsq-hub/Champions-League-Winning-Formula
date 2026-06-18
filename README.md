# Champions League Winning Formula ⚽📊

## Overview

This project analyzes UEFA Champions League team performance using football statistics and builds a quantitative model to identify the factors behind successful teams.

The goal is to answer:

**What statistical characteristics define a strong Champions League team?**

---

## Research Question

Can attacking performance and defensive stability predict a team's competitive strength in the Champions League?

---

## Dataset

Source:
- FBref UEFA Champions League Statistics

The dataset contains team-level performance metrics including:

- Goals scored
- Goals conceded
- Possession
- Assists
- Match performance statistics

---

## Methodology

The analysis pipeline:

1. Collect Champions League team statistics
2. Clean and process raw data
3. Combine attacking and defensive performance
4. Calculate performance indicators

Key metrics:

### Goals For (GF)

Measures attacking output.

### Goals Against (GA)

Measures defensive stability.

### Goal Difference (GD)

Formula:

GD = GF - GA

### Winning Formula Score

A weighted performance model:

Winning Score =
0.4 × Attack
- 0.4 × Defense
+ 0.2 × Goal Difference

---

## Results

Top performing teams based on the model:

| Team | GF | GA | GD |
|----|----|----|----|
| Bayern Munich | 42 | 19 | +23 |
| Paris Saint-Germain | 45 | 23 | +22 |
| Barcelona | 31 | 18 | +13 |
| Real Madrid | 32 | 20 | +12 |

---

## Key Findings

The analysis suggests:

- Elite Champions League teams require both strong attacking output and defensive stability.
- High-scoring teams are not always the strongest overall teams.
- Balanced performance is a key factor in tournament success.

---

## Visualization

The project includes:

- Goal Difference ranking charts
- Team performance comparisons

---

## Tools

Python

Libraries:
- Pandas
- Matplotlib

---

## Future Improvements

Possible extensions:

- Add expected goals (xG)
- Add passing and pressing metrics
- Build machine learning prediction models
- Create an interactive dashboard using Streamlit