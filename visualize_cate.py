import pandas as pd
import plotly.express as px
import plotly.io as pio

# 1. Load the CATE data
df = pd.read_csv("netflix_cate_data.csv")

# 2. Create the Strategic ROI Map
fig = px.scatter(
    df, x="genre_pop", y="predicted_lift",
    trendline="ols",
    color="predicted_lift",
    color_continuous_scale=['#564d4d', '#E50914'],
    title="Marketing Efficiency Curve: Diminishing Returns by Popularity",
    labels={
        'genre_pop': 'Genre Popularity (0-100)',
        'predicted_lift': 'Marginal Viewership Lift (M Hours)'
    },
    template="plotly_dark"
)

# 3. Add Strategic Annotations
fig.add_annotation(
    x=10, y=11, text="<b>High ROI Zone</b><br>Target for Growth",
    showarrow=True, arrowhead=1, bgcolor="#E50914"
)
fig.add_annotation(
    x=90, y=3, text="<b>Saturation Zone</b><br>Diminishing Returns",
    showarrow=True, arrowhead=1, bgcolor="#564d4d"
)

# 4. Save to the existing Report
with open('causal_report.html', 'a') as f:
    f.write("<br><hr><br>") # Add a visual separator
    f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))

print("Phase 9 complete: Efficiency Curve added to 'causal_report.html'.")
