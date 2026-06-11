# Netflix Content ROI · Causal Inference

**Does marketing spend actually drive viewership — or does it just follow popular content?**

A causal inference framework that corrects for selection bias in Netflix-style marketing data, revealing a **10.9× ROI gap** between niche and blockbuster content strategies.

🚀 **[Live App →](https://04-snigdha-netflix-causal-project-streamlit-app.streamlit.app)**

---

## Key Results

| Metric | Value |
|:---|:---|
| Naive ATE (correlation) | 8.7M viewership hours |
| Causal ATE (backdoor-corrected) | 1.4M viewership hours |
| Bias in naive estimate | +535% overestimate |
| Niche content lift | 4.0M hrs |
| Blockbuster content lift | 0.37M hrs |
| ROI gap (niche ÷ blockbuster) | **10.9×** |

---

## The Problem

Marketing budgets tend to follow popular titles — blockbusters and holiday releases already attract audiences organically, yet they receive the largest budgets. Naive correlation-based analysis therefore *overestimates* the ROI of marketing by conflating organic viewership with caused viewership.

## The Approach

1. **DAG modelling** — "Holiday Season" is specified as a confounder that drives both budget allocation and organic viewership.
2. **Backdoor criterion** — OLS regression blocks the confounding path to isolate the true causal effect of marketing spend.
3. **X-Learner (CATE)** — A meta-learner estimates individual treatment effects, revealing that niche titles benefit ~10.9× more from marketing than blockbusters.
4. **Refutation tests** — Placebo treatment and data subset tests confirm the model is not capturing spurious correlations.

## Technical Stack

- **Causal inference**: DoWhy, backdoor criterion, X-Learner meta-learner
- **Modelling**: scikit-learn (Linear Regression, Propensity Score Weighting)
- **Visualisation**: Plotly, Streamlit
- **Data**: 2,000 synthetic Netflix titles with engineered confounding structure

## Run Locally

```bash
git clone https://github.com/04-snigdha/netflix-causal-project.git
cd netflix-causal-project
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Or run the analysis scripts directly:

```bash
python generate_data.py       # generate synthetic dataset
python causal_analysis.py     # ATE + refutation tests
python cate_analysis.py       # X-Learner CATE
python visualize_results.py   # static Plotly charts
```

---

*Built by [Snigdha Sharma](https://github.com/04-snigdha) · VU Amsterdam BSc AI*
