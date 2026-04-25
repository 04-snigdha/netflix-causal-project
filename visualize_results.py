import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.formula.api as smf

def main():
    print("Loading data...")
    df = pd.read_csv('netflix_data.csv')

    print("Generating Scatter Plot...")
    # Scatter plot of Viewership vs Genre Popularity
    # Color or size by marketing spend
    fig_scatter = px.scatter(
        df, 
        x='genre_popularity', 
        y='viewership_hours', 
        color='marketing_spend',
        title='Viewership vs Genre Popularity (Colored by Marketing Spend)',
        labels={
            'genre_popularity': 'Genre Popularity (0-10)',
            'viewership_hours': 'Viewership (Thousands of Hours)',
            'marketing_spend': 'Marketing Spend ($K)'
        },
        template='plotly_dark'
    )
    
    # Save as HTML
    fig_scatter.write_html('scatter_plot.html')
    print("Saved scatter_plot.html")

    print("Calculating Lifts...")
    # 1. Correlation-based Lift (Naive Regression without Confounders)
    # y = b0 + b1*T
    naive_model = smf.ols('viewership_hours ~ marketing_spend', data=df).fit()
    naive_lift = naive_model.params['marketing_spend']

    # 2. Causal ATE Lift (Controlling for Confounders)
    # y = b0 + b1*T + b2*W1 + b3*W2
    causal_model = smf.ols('viewership_hours ~ marketing_spend + is_holiday_season + genre_popularity', data=df).fit()
    causal_lift = causal_model.params['marketing_spend']

    print("Generating Bar Chart...")
    # Bar Chart comparing Naive vs Causal
    fig_bar = go.Figure(data=[
        go.Bar(
            name='Lift Estimate', 
            x=['Correlation-based Lift (Naive)', 'Causal ATE (Controlled)'], 
            y=[naive_lift, causal_lift],
            marker_color=['indianred', 'lightsalmon']
        )
    ])
    
    # True causal effect in generate_data.py was 1.5
    fig_bar.add_hline(y=1.5, line_dash="dash", line_color="white", annotation_text="True Causal Effect (1.5)", annotation_position="top right")

    fig_bar.update_layout(
        title='Why Causality Matters: Naive vs Causal Estimate of Marketing Lift',
        yaxis_title='Estimated Lift in Viewership per $1K Spend',
        template='plotly_dark'
    )

    # Save as HTML
    fig_bar.write_html('bar_chart.html')
    print("Saved bar_chart.html")

if __name__ == "__main__":
    main()
