# Netflix Content Success Predictor: A Causal Inference Study

## Executive Summary
This project demonstrates the power of Causal Machine Learning in separating true Marketing ROI from seasonal trends. We built a synthetic Netflix dataset and applied causal inference techniques to isolate the actual impact of marketing spend on viewership hours, untangling it from organic holiday spikes.

## The Challenge
In our dataset, we face a classic **Confounding Bias**. 
The "Holiday Season" affects both our variables:
1. **Marketing Spend**: The marketing team naturally spends more during the holidays.
2. **Viewership**: Netflix viewership organically spikes during the holidays.

If we look at a standard correlation, the model mistakenly attributes the massive holiday viewership spike directly to the marketing spend.

## The Results
By using the `DoWhy` causal framework and applying the Backdoor Criterion, we successfully controlled for the confounder:

- **Naive Correlation (Lift)**: `11.07M Hours` (Heavily inflated)
- **Causal Impact (ATE)**: `5.42M Hours` (The True Impact)

*Note: The causal model successfully passed all DoWhy Refutation tests (Placebo Treatment, Random Common Cause, and Data Subset refuters), proving the robustness of the 5.42M estimate.*

## Tech Stack
- **Python**
- **DoWhy** (Causal Inference)
- **Pandas** (Data Engineering)
- **Plotly** (Interactive Visualization)

## How to Run
Follow this order to replicate the study:
1. `python generate_data.py` - Generates the synthetic biased dataset (`netflix_data.csv`).
2. `python causal_analysis.py` - Runs the DoWhy causal model, estimates the ATE, and executes the refutation robustness tests.
3. `python visualize_results.py` - Generates the interactive HTML visualization (`causal_report.html`) to compare the Naive vs. Causal results.
4. `python cate_analysis.py` - Calculates the Conditional Average Treatment Effect (CATE) using an X-Learner.
5. `python visualize_cate.py` - Appends the efficiency curve to the HTML report.

## 🚀 Phase 2: Strategic ROI Optimization (CATE)
In the second season of our study, we moved beyond average impacts to discover **Heterogeneous Treatment Effects**. By employing an X-Learner meta-learner, we unmasked the "Diminishing Returns" of marketing spend. 

### The Data
The analysis revealed that marketing effectiveness is heavily dependent on the underlying baseline popularity of a genre:
- **Niche Content (Low Popularity)**: Generates a massive **10.95M Hours** of lift.
- **Blockbuster Content (High Popularity)**: Generates only **3.75M Hours** of lift.

Marketing lift is therefore **~2.9x higher** for unknown/niche content compared to established blockbusters.

**Business Impact: By reallocating 20% of the marketing budget from high-popularity hits to niche genre titles, Netflix can achieve a significantly higher net viewership lift per dollar spent.**
