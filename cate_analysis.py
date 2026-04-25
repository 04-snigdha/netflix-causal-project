import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import os

try:
    from causalml.inference.meta import XLearner
except ImportError:
    print("causalml not found. Using fallback SimpleXLearner.")
    class XLearner:
        def __init__(self, models):
            from sklearn.base import clone
            self.m0 = clone(models)
            self.m1 = clone(models)
            self.te0 = clone(models)
            self.te1 = clone(models)
        
        def fit_predict(self, X, T, y):
            X, T, y = np.array(X), np.array(T), np.array(y)
            X0, y0 = X[T==0], y[T==0]
            X1, y1 = X[T==1], y[T==1]
            self.m0.fit(X0, y0)
            self.m1.fit(X1, y1)
            D1 = y1 - self.m0.predict(X1)
            D0 = self.m1.predict(X0) - y0
            self.te1.fit(X1, D1)
            self.te0.fit(X0, D0)
            return 0.5 * self.te0.predict(X) + 0.5 * self.te1.predict(X)

# 1. Load Data
df = pd.read_csv("netflix_data.csv")

# 2. Prepare Variables
X = df[['genre_pop', 'is_holiday']]
T = df['marketing_spend']
y = df['viewership']

# 3. Initialize X-Learner
# Using LinearRegression as the base learner for simplicity/interpretability
learner = XLearner(models=LinearRegression())

# 4. Estimate Individual Treatment Effects (ITE)
# This calculates: What would be the lift for THIS specific movie?
ite = learner.fit_predict(X, T, y)
df['predicted_lift'] = ite

# 5. Segment Analysis
niche_lift = df[df['genre_pop'] < 25]['predicted_lift'].mean()
blockbuster_lift = df[df['genre_pop'] > 75]['predicted_lift'].mean()

print("-" * 30)
print(f"AVERAGE LIFT FOR NICHE CONTENT (<25 Pop): {niche_lift:.2f}M Hours")
print(f"AVERAGE LIFT FOR BLOCKBUSTERS (>75 Pop): {blockbuster_lift:.2f}M Hours")
print("-" * 30)

# Save the ITE data for the next visualization phase
df.to_csv("netflix_cate_data.csv", index=False)
