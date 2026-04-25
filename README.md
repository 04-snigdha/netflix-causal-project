# Content Success Predictor: Causal Inference for Marketing Optimization

## Executive Summary
This project implements a causal inference framework to determine the true impact of marketing spend on Netflix viewership. By moving beyond simple correlation, the study isolates the causal "lift" of marketing activities while controlling for significant confounders such as release seasonality (Holiday Effect) and inherent genre popularity.

## The STAR Method Analysis

### Situation
In the streaming industry, marketing budgets are often allocated to titles that are already predisposed to success (e.g., blockbusters or holiday releases). This creates a "selection bias" where high viewership is attributed to marketing spend, when it may actually be driven by organic seasonal trends. Standard regression models fail to account for this confounding, leading to inflated ROI estimates and inefficient capital allocation.

### Task
The objective was to build a robust causal pipeline to:
- Identify the Average Treatment Effect (ATE) of marketing spend on viewership.
- Differentiate between correlation and causation in viewership spikes.
- Calculate the Conditional Average Treatment Effect (CATE) to identify which content segments (Niche vs. Blockbuster) yield the highest marginal ROI for every dollar spent on marketing.

### Action
- **Data Engineering**: Developed a synthetic dataset of 2,000 titles, incorporating a hidden confounding structure where "Holiday Season" influenced both marketing budget allocation and organic viewership.
- **Causal Modeling**: Utilized the DoWhy library to define a Directed Acyclic Graph (DAG), identifying the Backdoor Criterion required to neutralize confounding bias.
- **Estimation Logic**: Implemented Propensity Score Weighting and Linear Regression estimators to calculate the true causal lift.
- **Meta-Learning**: Applied an X-Learner (Meta-Learner) logic to estimate Heterogeneous Treatment Effects, allowing for the calculation of individualized lift for every title.
- **Robustness Testing**: Conducted Placebo Treatment and Data Subset refutation tests to validate the model's sensitivity to unobserved noise.

### Result
- **Unmasked Bias**: Demonstrated that a naive correlation-based approach overestimated marketing impact by over 100% (11.07M naive lift vs. 5.42M causal ATE).
- **Strategic ROI Discovery**: Identified that marketing spend is approximately 2.9x more effective for niche content (10.95M lift) compared to established blockbusters (3.75M lift).
- **Model Reliability**: Passed all refutation tests with p-values > 0.05 on placebo treatments, confirming the model did not capture spurious correlations.

## Technical Stack
- **Language**: Python
- **Causal Framework**: DoWhy, Scikit-Learn
- **Data Analysis**: Pandas, NumPy, Statsmodels
- **Visualization**: Plotly (Interactive HTML Reporting)

## Key Findings

| Metric | Naive Estimate (Correlation) | Causal Estimate (Truth) | Variance |
| :--- | :--- | :--- | :--- |
| **Viewership Lift** | 11.07 Million Hours | 5.42 Million Hours | -51.0% |
| **Niche Segment ROI** | N/A | 10.95 Million Hours | High ROI |
| **Blockbuster ROI** | N/A | 3.75 Million Hours | Saturation |

## Business Impact and Recommendations
The study reveals that marketing budgets are frequently "saturated" on high-popularity titles. By reallocating a portion of the marketing spend from guaranteed hits (Blockbusters) to high-potential Niche titles, the organization can achieve a significantly higher net viewership lift per dollar spent. This framework provides a data-driven path to maximizing global viewing hours through strategic budget redistribution.

## Implementation Guide
To replicate the study, execute the scripts in the following order:
1. `generate_data.py`: Creates the biased dataset with holiday confounders.
2. `causal_analysis.py`: Performs the ATE identification and refutation tests.
3. `cate_analysis.py`: Calculates the individualized treatment effects (CATE).
4. `visualize_results.py` and `visualize_cate.py`: Generates the interactive Causal Reports.
