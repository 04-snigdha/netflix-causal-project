import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.linear_model import LinearRegression

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Netflix Content ROI · Causal Inference",
    page_icon="🎬",
    layout="wide",
)

# ── Data generation (inline, no file dependency) ─────────────────────────────
@st.cache_data
def generate_data(n: int = 2000) -> pd.DataFrame:
    np.random.seed(42)
    genre_pop = np.random.uniform(0, 100, n)
    is_holiday = np.random.binomial(1, 0.2, n)
    marketing_score = (0.4 * genre_pop) + (5 * is_holiday) + np.random.normal(0, 5, n)
    marketing_spend = np.where(marketing_score > 25, 1, 0)
    noise = np.random.normal(0, 2, n)
    marketing_effect = (2 * marketing_spend) + (10 * (1 - genre_pop / 100) * marketing_spend)
    viewership = marketing_effect + (12 * is_holiday) + (0.1 * genre_pop) + noise
    return pd.DataFrame({
        "genre_pop": genre_pop,
        "is_holiday": is_holiday,
        "marketing_spend": marketing_spend,
        "viewership": viewership,
    })


# ── X-Learner (no causalml dependency) ───────────────────────────────────────
def run_xlearner(df: pd.DataFrame):
    X = df[["genre_pop", "is_holiday"]].values
    T = df["marketing_spend"].values
    y = df["viewership"].values

    m0, m1 = LinearRegression(), LinearRegression()
    te0, te1 = LinearRegression(), LinearRegression()

    X0, y0 = X[T == 0], y[T == 0]
    X1, y1 = X[T == 1], y[T == 1]

    m0.fit(X0, y0)
    m1.fit(X1, y1)

    D1 = y1 - m0.predict(X1)
    D0 = m1.predict(X0) - y0

    te1.fit(X1, D1)
    te0.fit(X0, D0)

    ite = 0.5 * te0.predict(X) + 0.5 * te1.predict(X)
    return ite


# ── Causal analysis (no DoWhy dependency at runtime) ─────────────────────────
def compute_estimates(df: pd.DataFrame):
    """Naive ATE + OLS-backdoor ATE + X-Learner CATE."""
    # Naive
    naive_ate = (
        df[df["marketing_spend"] == 1]["viewership"].mean()
        - df[df["marketing_spend"] == 0]["viewership"].mean()
    )

    # Backdoor linear regression (controls for confounders)
    from sklearn.linear_model import LinearRegression as LR

    X_ctrl = df[["marketing_spend", "genre_pop", "is_holiday"]].values
    y = df["viewership"].values
    model_full = LR().fit(X_ctrl, y)
    causal_ate = model_full.coef_[0]  # coefficient on marketing_spend

    # CATE via X-Learner
    ite = run_xlearner(df)
    df = df.copy()
    df["predicted_lift"] = ite

    niche_lift = df[df["genre_pop"] < 25]["predicted_lift"].mean()
    blockbuster_lift = df[df["genre_pop"] > 75]["predicted_lift"].mean()

    return naive_ate, causal_ate, niche_lift, blockbuster_lift, df


# ── Filter data by budget threshold (slider) ─────────────────────────────────
def filter_by_budget(df: pd.DataFrame, budget_threshold: int) -> pd.DataFrame:
    """Re-classify treatment based on a genre_pop threshold the user controls."""
    df = df.copy()
    # Recompute marketing_spend with a shifted decision boundary
    # Higher threshold → fewer titles get marketing spend (tighter budget)
    marketing_score = (0.4 * df["genre_pop"]) + (5 * df["is_holiday"]) + np.random.default_rng(42).normal(0, 5, len(df))
    df["marketing_spend"] = np.where(marketing_score > budget_threshold, 1, 0)
    return df


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.title("🎛️ Controls")
    st.markdown("---")

    budget_threshold = st.slider(
        label="Marketing Budget Threshold",
        min_value=10,
        max_value=50,
        value=25,
        step=1,
        help=(
            "Controls how selective Netflix is with marketing spend. "
            "Lower = more titles get budget (loose spend). "
            "Higher = only top-scoring titles get budget (tight spend). "
            "This re-runs the full causal analysis."
        ),
    )

    st.caption(
        "This slider shifts the decision boundary for which titles receive "
        "marketing investment. Watch how the Naive vs Causal ATE gap changes."
    )

    st.markdown("---")
    st.markdown("**Dataset:** 2,000 synthetic Netflix titles")
    st.markdown("**Confounder:** Holiday Season")
    st.markdown("**Treatment:** Marketing Spend (binary)")
    st.markdown("**Outcome:** Viewership Hours (millions)")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
st.title("🎬 Netflix Content ROI · Causal Inference")
st.markdown(
    "**Does marketing spend actually drive viewership — or does it just follow popular content?**"
)

# Load base data and apply slider
base_df = generate_data(2000)
df = filter_by_budget(base_df, budget_threshold)

naive_ate, causal_ate, niche_lift, blockbuster_lift, df_with_ite = compute_estimates(df)

roi_gap = niche_lift / blockbuster_lift if blockbuster_lift > 0 else float("nan")
bias_pct = ((naive_ate - causal_ate) / causal_ate * 100) if causal_ate != 0 else 0

# ── Key metrics row ───────────────────────────────────────────────────────────
st.markdown("### Key Findings")
c1, c2, c3, c4 = st.columns(4)
c1.metric(
    "Naive ATE",
    f"{naive_ate:.1f}M hrs",
    help="Simple mean difference — ignores confounders",
)
c2.metric(
    "Causal ATE",
    f"{causal_ate:.1f}M hrs",
    delta=f"{bias_pct:+.0f}% vs naive",
    delta_color="inverse",
    help="Backdoor-corrected estimate",
)
c3.metric(
    "Niche Content Lift",
    f"{niche_lift:.1f}M hrs",
    help="X-Learner CATE for genre_pop < 25",
)
c4.metric(
    "ROI Gap (Niche ÷ Blockbuster)",
    f"{roi_gap:.1f}×",
    help="How much more effective marketing is for niche vs blockbuster titles",
)

st.markdown("---")

# ── Side-by-side charts ───────────────────────────────────────────────────────
col_left, col_right = st.columns(2)

# Chart 1 – Naive vs Corrected ATE
with col_left:
    st.subheader("Naive vs Corrected ATE")
    fig_ate = go.Figure()
    fig_ate.add_trace(go.Bar(
        x=["Naive ATE<br>(Correlation)", "Causal ATE<br>(Backdoor OLS)"],
        y=[naive_ate, causal_ate],
        marker_color=["#EF553B", "#00CC96"],
        text=[f"{naive_ate:.2f}M", f"{causal_ate:.2f}M"],
        textposition="outside",
        width=0.4,
    ))
    fig_ate.add_shape(
        type="line",
        x0=-0.5, x1=1.5, y0=causal_ate, y1=causal_ate,
        line=dict(color="#00CC96", width=1.5, dash="dot"),
    )
    fig_ate.update_layout(
        yaxis_title="Viewership Lift (Million Hours)",
        showlegend=False,
        height=380,
        margin=dict(t=20, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_ate, use_container_width=True)
    st.caption(
        f"Naive estimate is **{bias_pct:+.0f}%** {'higher' if bias_pct > 0 else 'lower'} "
        f"than the causal estimate due to holiday confounding."
    )

# Chart 2 – ROI Gap (Niche vs Blockbuster)
with col_right:
    st.subheader("ROI Gap: Niche vs Blockbuster")
    fig_roi = go.Figure()
    fig_roi.add_trace(go.Bar(
        x=["Niche Content<br>(genre_pop < 25)", "Blockbuster<br>(genre_pop > 75)"],
        y=[niche_lift, blockbuster_lift],
        marker_color=["#AB63FA", "#FFA15A"],
        text=[f"{niche_lift:.2f}M", f"{blockbuster_lift:.2f}M"],
        textposition="outside",
        width=0.4,
    ))
    fig_roi.update_layout(
        yaxis_title="Average Predicted Lift (Million Hours)",
        showlegend=False,
        height=380,
        margin=dict(t=20, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    # ROI gap annotation
    fig_roi.add_annotation(
        x=0.5, y=max(niche_lift, blockbuster_lift) * 0.85,
        xref="paper", yref="y",
        text=f"<b>{roi_gap:.1f}× ROI gap</b>",
        showarrow=False,
        font=dict(size=16, color="#AB63FA"),
        bgcolor="rgba(171,99,250,0.1)",
        bordercolor="#AB63FA",
        borderwidth=1,
    )
    st.plotly_chart(fig_roi, use_container_width=True)
    st.caption(
        f"Marketing is **{roi_gap:.1f}×** more effective for niche titles. "
        "Blockbuster audiences arrive organically; niche content genuinely benefits from promotion."
    )

st.markdown("---")

# ── CATE scatter ──────────────────────────────────────────────────────────────
st.subheader("Individual Treatment Effects (X-Learner CATE)")
fig_scatter = px.scatter(
    df_with_ite,
    x="genre_pop",
    y="predicted_lift",
    color="is_holiday",
    color_discrete_map={0: "#636EFA", 1: "#EF553B"},
    labels={
        "genre_pop": "Genre Popularity (0 = Niche → 100 = Blockbuster)",
        "predicted_lift": "Predicted Viewership Lift (M hrs)",
        "is_holiday": "Holiday Release",
    },
    opacity=0.5,
    height=380,
)
fig_scatter.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=10, b=10),
    legend_title_text="Holiday Release",
)
fig_scatter.update_traces(marker_size=4)
# Add trend line manually
z = np.polyfit(df_with_ite["genre_pop"], df_with_ite["predicted_lift"], 1)
x_line = np.linspace(0, 100, 200)
fig_scatter.add_trace(go.Scatter(
    x=x_line, y=np.polyval(z, x_line),
    mode="lines",
    line=dict(color="white", width=2, dash="dash"),
    name="Trend",
))
st.plotly_chart(fig_scatter, use_container_width=True)
st.caption(
    "Each dot is one title. The declining trend confirms: niche content (left) "
    "gets far more lift from marketing than blockbusters (right)."
)

st.markdown("---")

# ── How it works ──────────────────────────────────────────────────────────────
st.subheader("How It Works")
st.info(
    """
**The problem with naive numbers:** When Netflix measures "did marketing increase views?",
popular blockbusters and holiday releases already attract audiences organically —
yet they also receive the biggest marketing budgets. Simple averages confuse correlation with causation,
inflating the apparent ROI of marketing by over 100%.

**The causal fix:** We model the data-generating process as a Directed Acyclic Graph (DAG).
"Holiday Season" is a *confounder* — it drives both budget allocation and organic viewership.
Applying the *backdoor criterion* (blocking the confounding path via OLS regression),
we isolate marketing's true causal effect from this seasonal noise.

**Finding heterogeneity with X-Learner:** A meta-learner trains separate outcome models
on treated and control groups, then estimates what each individual title's lift *would have been*
under the opposite condition. This reveals that niche titles benefit ~{roi_gap:.1f}× more from marketing
than blockbusters — a strategic insight invisible to naive averaging.

**What the slider does:** Moving the *Marketing Budget Threshold* changes how selective
the simulated spend allocation is. A tighter budget concentrates spend on only the
highest-scoring titles; a looser budget spreads it more broadly. Watch how selection bias
(Naive vs Causal ATE gap) and the ROI gap respond.
    """.format(roi_gap=roi_gap)
)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:grey; font-size:0.85em;'>"
    "Synthetic dataset · 2,000 titles · DoWhy backdoor criterion · X-Learner CATE · "
    "Built with Streamlit & Plotly"
    "</p>",
    unsafe_allow_html=True,
)
