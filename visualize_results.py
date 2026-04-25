import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Load Data
df = pd.read_csv("netflix_data.csv")

# 2. Create the Scatter Plot (The Confounder View)
fig1 = px.scatter(
    df, x="genre_pop", y="viewership",
    color="marketing_spend",
    symbol="is_holiday",
    title="Netflix Viewership: Marketing Lift vs. Holiday Confounding",
    labels={'marketing_spend': 'Marketing Spend', 'is_holiday': 'Holiday Release'},
    template="plotly_dark",
    color_discrete_map={0: '#221F1F', 1: '#E50914'} # Netflix Colors
)

# 3. Create the Comparison Bar Chart (The 'Truth' View)
# Using your actual Phase 3 results
metrics = ['Naive Lift (Correlation)', 'Causal ATE (True Impact)']
values = [11.07, 5.42]

fig2 = px.bar(
    x=metrics, y=values,
    color=metrics,
    title="Budget Accuracy: Naive vs. Causal Estimates",
    labels={'x': 'Analysis Method', 'y': 'Hours (Millions)'},
    template="plotly_dark",
    color_discrete_sequence=['#564d4d', '#E50914']
)

# 4. Save to HTML
# Writing 'w' instead of 'a' so it creates fresh or overwrites cleanly
with open('causal_report.html', 'w') as f:
    f.write(fig1.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig2.to_html(full_html=False, include_plotlyjs='cdn'))

print("Visualization complete: 'causal_report.html' created.")
