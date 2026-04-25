import numpy as np
import pandas as pd

np.random.seed(42)
n_samples = 10000

# Confounder
# 1 if holiday season, 0 otherwise. Let's say 30% of the year is holiday season.
is_holiday_season = np.random.binomial(1, 0.3, n_samples)

# Other variable
# Genre popularity score from 0 to 10
genre_popularity = np.random.uniform(0, 10, n_samples)

# Treatment: Marketing Spend (in thousands of dollars)
# Marketing spend is higher during the holiday season.
marketing_spend = np.random.normal(50 + 30 * is_holiday_season + 2 * genre_popularity, 10, n_samples)
marketing_spend = np.maximum(0, marketing_spend)

# Outcome: Viewership hours (in thousands of hours)
# Causal effect of marketing spend: Let's set True ATE = 1.5
# Holiday season also directly increases viewership (confounder effect).
# Genre popularity also increases viewership.
viewership_hours = np.random.normal(10 + 1.5 * marketing_spend + 50 * is_holiday_season + 5 * genre_popularity, 15, n_samples)
viewership_hours = np.maximum(0, viewership_hours)

df = pd.DataFrame({
    'genre_popularity': genre_popularity,
    'is_holiday_season': is_holiday_season,
    'marketing_spend': marketing_spend,
    'viewership_hours': viewership_hours
})

df.to_csv('netflix_data.csv', index=False)
print("Synthetic data successfully generated and saved to netflix_data.csv")
