# Netflix Causal Predictor

## Executive Summary
This project demonstrates the importance of causal inference in marketing analytics. We built a synthetic dataset to model the effect of marketing spend on Netflix viewership hours. By applying causal inference techniques using the `DoWhy` library, we were able to isolate the true Average Treatment Effect (ATE) of marketing spend, separating it from spurious correlations.

## The Confounder: Holiday Season
In our synthetic dataset, the "Holiday Season" acts as a hidden confounder. 
- During the holidays, Netflix naturally experiences an organic increase in **viewership**.
- Concurrently, the marketing team increases their **marketing spend** during the holidays.

If we use a naive correlation or standard regression model without controlling for the confounder, the model attributes the organic holiday traffic to the marketing spend, resulting in an artificially inflated estimate of marketing effectiveness. By defining a causal graph and applying the backdoor criterion, our causal model correctly accounts for the holiday season, estimating the true lift of marketing spend.

## How to Run

1. **Install Requirements**:
   Ensure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate Data**:
   Generate the synthetic dataset (`netflix_data.csv`) containing the hidden confounder:
   ```bash
   python generate_data.py
   ```

3. **Causal Analysis**:
   Run the causal modeling script to estimate the ATE and perform robustness checks (Placebo and Random Common Cause):
   ```bash
   python causal_analysis.py
   ```

4. **Visualization**:
   Generate Plotly visualizations comparing the naive correlation lift against the causal ATE:
   ```bash
   python visualize_results.py
   ```
   This will output two HTML files: `scatter_plot.html` and `bar_chart.html` that can be opened in any web browser.
