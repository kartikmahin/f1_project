"""Streamlit dashboard for Universal F1 Race Predictor.

Supports any Grand Prix — past, present, or future.
For past races: shows real results vs predicted positions side-by-side.
For future races: shows predictions only with an "upcoming" banner.

Run with: streamlit run dashboard.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from config import (
    DRIVERS_2026, DRIVER_NAMES, TEAM_COLORS, FEATURE_COLUMNS,
    F1_CALENDAR, get_gp_list, get_race_date, is_race_in_past,
)
from race_predictor import predict_race, get_team_color


# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="F1 Race Predictor",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS for a premium dark theme
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global dark theme */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
    }

    /* Custom header */
    .race-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    .race-header h1 {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #e94560, #ff6b6b, #ffa500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .race-header .subtitle {
        color: #8b949e;
        font-size: 1rem;
        font-weight: 400;
    }

    /* Status banners */
    .status-past {
        background: linear-gradient(135deg, #0d3320 0%, #064e2b 100%);
        border: 1px solid #238636;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-bottom: 1.5rem;
        color: #56d364;
        font-weight: 500;
        font-size: 1.05rem;
    }
    .status-future {
        background: linear-gradient(135deg, #3d1f00 0%, #4a2600 100%);
        border: 1px solid #d29922;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-bottom: 1.5rem;
        color: #e3b341;
        font-weight: 500;
        font-size: 1.05rem;
    }

    /* Podium cards */
    .podium-card {
        background: linear-gradient(145deg, #1c1c2e, #252540);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.06);
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        transition: transform 0.2s ease;
    }
    .podium-card:hover {
        transform: translateY(-4px);
    }
    .podium-card .position {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
    }
    .podium-card .driver-name {
        font-size: 1.15rem;
        font-weight: 700;
        color: #e6edf3;
        margin-bottom: 0.2rem;
    }
    .podium-card .team-name {
        font-size: 0.85rem;
        color: #8b949e;
        margin-bottom: 0.5rem;
    }
    .gold { border-top: 3px solid #FFD700; }
    .gold .position { color: #FFD700; }
    .silver { border-top: 3px solid #C0C0C0; }
    .silver .position { color: #C0C0C0; }
    .bronze { border-top: 3px solid #CD7F32; }
    .bronze .position { color: #CD7F32; }

    /* Accuracy metric cards */
    .metric-card {
        background: linear-gradient(145deg, #1c1c2e, #252540);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.06);
    }
    .metric-card .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #58a6ff;
    }
    .metric-card .metric-label {
        font-size: 0.8rem;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Section headers */
    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #e6edf3;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(255,255,255,0.06);
    }

    /* Comparison table highlight */
    .delta-positive { color: #56d364; }
    .delta-negative { color: #f85149; }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Sidebar — Race Selection
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🏎️ F1 Race Predictor")
    st.markdown("---")

    # Year selector
    selected_year = st.selectbox(
        "📅 Season",
        options=[2024, 2025, 2026],
        index=2,
        help="Select the F1 season"
    )

    # GP selector (in calendar order)
    gp_list = get_gp_list(selected_year)
    selected_gp = st.selectbox(
        "🏁 Grand Prix",
        options=gp_list,
        index=0,
        help="Select the race to predict"
    )

    # Show race date and status
    race_date = get_race_date(selected_year, selected_gp)
    is_past = is_race_in_past(selected_year, selected_gp)

    if race_date:
        st.markdown(f"**Date:** {race_date.strftime('%B %d, %Y')}")

    if is_past:
        st.success("✅ Race completed")
    else:
        st.warning("🔮 Race upcoming")

    st.markdown("---")

    # Navigation
    page = st.radio(
        "📊 View",
        ["Race Predictions", "Driver Analysis", "Model Training"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(
        "<div style='color:#8b949e; font-size:0.75rem; text-align:center;'>"
        "Neural Network Ensemble<br>with Uncertainty Estimation</div>",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Main content
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Page: Race Predictions
# ---------------------------------------------------------------------------
def _render_podium_card(driver, team, position_label, css_class, confidence=None, tag="PREDICTED"):
    """Render a single podium card."""
    full_name = DRIVER_NAMES.get(driver, driver)
    team_color = get_team_color(team)
    conf_text = f"<div style='font-size:0.8rem; color:#8b949e;'>Confidence: {confidence:.0%}</div>" if confidence else ""
    tag_color = "#56d364" if tag == "ACTUAL" else "#58a6ff"
    return f"""
    <div class="podium-card {css_class}">
        <div style="font-size:0.7rem; color:{tag_color}; text-transform:uppercase;
                    letter-spacing:1px; margin-bottom:0.3rem; font-weight:600;">{tag}</div>
        <div class="position">{position_label}</div>
        <div class="driver-name">{full_name}</div>
        <div class="team-name" style="color:{team_color};">{team}</div>
        {conf_text}
    </div>
    """


def show_predictions(year, gp_name):
    """Main predictions page."""
    # Header
    st.markdown(f"""
    <div class="race-header">
        <h1>🏁 {gp_name} {year}</h1>
        <div class="subtitle">Neural network ensemble predictions with uncertainty estimation</div>
    </div>
    """, unsafe_allow_html=True)

    # Run prediction
    with st.spinner("Generating predictions..."):
        result = predict_race(year, gp_name)

    predictions = result["predictions"]
    actual = result["actual_results"]
    comparison = result["comparison"]
    accuracy = result["accuracy"]

    # ─── Status Banner ───
    if result["status"] == "past":
        if actual is not None:
            st.markdown(
                '<div class="status-past">✅ This race has already happened — '
                'showing <strong>actual results</strong> alongside predictions for comparison.</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="status-past">✅ This race has already happened, '
                'but actual results could not be loaded. Showing predictions only.</div>',
                unsafe_allow_html=True,
            )
    else:
        race_date = get_race_date(year, gp_name)
        date_str = race_date.strftime("%B %d, %Y") if race_date else "TBD"
        st.markdown(
            f'<div class="status-future">🔮 This race hasn\'t happened yet (scheduled: {date_str}) '
            f'— showing <strong>predicted positions</strong> only.</div>',
            unsafe_allow_html=True,
        )

    # ─── PAST RACE: Actual Podium + Accuracy ───
    if result["status"] == "past" and actual is not None and not actual.empty:
        st.markdown('<div class="section-title">🏆 Actual Podium</div>', unsafe_allow_html=True)
        podium = actual.head(3)
        cols = st.columns(3)
        css_classes = ["gold", "silver", "bronze"]
        labels = ["🥇 P1", "🥈 P2", "🥉 P3"]
        for i, col in enumerate(cols):
            if i < len(podium):
                row = podium.iloc[i]
                col.markdown(
                    _render_podium_card(row["Driver"], row["Team"], labels[i], css_classes[i], tag="ACTUAL"),
                    unsafe_allow_html=True,
                )

        # Accuracy metrics
        if accuracy:
            st.markdown('<div class="section-title">📊 Prediction Accuracy</div>', unsafe_allow_html=True)
            m1, m2, m3, m4 = st.columns(4)
            m1.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{accuracy['mae']}</div>
                <div class="metric-label">Avg Position Error</div>
            </div>""", unsafe_allow_html=True)
            m2.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{accuracy['close_matches']}/{accuracy['total_drivers']}</div>
                <div class="metric-label">Within 3 Positions</div>
            </div>""", unsafe_allow_html=True)
            m3.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{accuracy['podium_accuracy']}</div>
                <div class="metric-label">Podium Correct</div>
            </div>""", unsafe_allow_html=True)
            m4.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{accuracy['exact_matches']}</div>
                <div class="metric-label">Exact Position</div>
            </div>""", unsafe_allow_html=True)

        # Side-by-side comparison table
        st.markdown('<div class="section-title">📋 Predicted vs Actual Standings</div>', unsafe_allow_html=True)
        if comparison is not None and not comparison.empty:
            display_comp = comparison[["Driver", "Team", "Actual", "Predicted", "Delta"]].copy()
            display_comp["Driver"] = display_comp["Driver"].map(lambda x: DRIVER_NAMES.get(x, x))
            display_comp["Predicted"] = display_comp["Predicted"].round(1)
            display_comp["Delta"] = display_comp["Delta"].round(1)
            display_comp.index = range(1, len(display_comp) + 1)
            display_comp.columns = ["Driver", "Team", "Actual Pos", "Predicted Pos", "Delta"]

            st.dataframe(
                display_comp.style.map(
                    lambda v: "color: #56d364" if isinstance(v, (int, float)) and v < 0
                    else ("color: #f85149" if isinstance(v, (int, float)) and v > 0 else ""),
                    subset=["Delta"]
                ),
                use_container_width=True,
                height=min(len(display_comp) * 40 + 40, 800),
            )

            # Predicted vs Actual chart
            st.markdown('<div class="section-title">📈 Predicted vs Actual Positions</div>', unsafe_allow_html=True)
            chart_df = comparison.copy()
            chart_df["DriverName"] = chart_df["Driver"].map(lambda x: DRIVER_NAMES.get(x, x))
            chart_df = chart_df.sort_values("Actual")

            fig = go.Figure()
            fig.add_trace(go.Bar(
                name="Actual Position",
                x=chart_df["DriverName"],
                y=chart_df["Actual"],
                marker_color=[get_team_color(t) for t in chart_df["Team"]],
                opacity=0.9,
            ))
            fig.add_trace(go.Scatter(
                name="Predicted Position",
                x=chart_df["DriverName"],
                y=chart_df["Predicted"],
                mode="markers+lines",
                marker=dict(size=10, color="#ff6b6b", symbol="diamond"),
                line=dict(color="#ff6b6b", width=2, dash="dot"),
            ))
            fig.update_layout(
                title="",
                yaxis_title="Position",
                xaxis_title="",
                showlegend=True,
                height=500,
                yaxis=dict(autorange="reversed"),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e6edf3"),
                legend=dict(bgcolor="rgba(0,0,0,0)"),
            )
            st.plotly_chart(fig, use_container_width=True)

    # ─── Predicted Podium (always shown) ───
    st.markdown('<div class="section-title">🔮 Predicted Podium</div>', unsafe_allow_html=True)
    pred_podium = predictions.head(3)
    cols = st.columns(3)
    css_classes = ["gold", "silver", "bronze"]
    labels = ["🥇 P1", "🥈 P2", "🥉 P3"]
    for i, col in enumerate(cols):
        if i < len(pred_podium):
            row = pred_podium.iloc[i]
            col.markdown(
                _render_podium_card(
                    row["Driver"], row["Team"], labels[i], css_classes[i],
                    confidence=row["Confidence"], tag="PREDICTED"
                ),
                unsafe_allow_html=True,
            )

    # ─── Full Predicted Grid ───
    st.markdown('<div class="section-title">📊 Full Predicted Grid</div>', unsafe_allow_html=True)
    display_pred = predictions[["Driver", "Team", "PredictedPosition", "Uncertainty", "Confidence"]].copy()
    display_pred["Driver"] = display_pred["Driver"].map(lambda x: DRIVER_NAMES.get(x, x))
    display_pred.columns = ["Driver", "Team", "Predicted Position", "Uncertainty (±)", "Confidence"]
    display_pred["Predicted Position"] = display_pred["Predicted Position"].round(1)
    display_pred["Uncertainty (±)"] = display_pred["Uncertainty (±)"].round(1)
    display_pred["Confidence"] = display_pred["Confidence"].apply(lambda x: f"{x:.0%}")
    st.dataframe(display_pred, use_container_width=True)

    # ─── Uncertainty Chart ───
    st.markdown('<div class="section-title">📉 Predicted Positions with Uncertainty</div>', unsafe_allow_html=True)
    fig2 = go.Figure()
    for idx, row in predictions.iterrows():
        team_color = get_team_color(row["Team"])
        fig2.add_trace(go.Bar(
            name=DRIVER_NAMES.get(row["Driver"], row["Driver"]),
            x=[DRIVER_NAMES.get(row["Driver"], row["Driver"])],
            y=[row["PredictedPosition"]],
            error_y=dict(type="data", array=[row["Uncertainty"]], visible=True),
            marker_color=team_color,
            hovertext=f"{row['Team']}<br>Confidence: {row['Confidence']:.0%}",
            showlegend=False,
        ))
    fig2.update_layout(
        title="",
        yaxis_title="Predicted Position",
        xaxis_title="",
        height=500,
        yaxis=dict(autorange="reversed"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e6edf3"),
    )
    st.plotly_chart(fig2, use_container_width=True)

    # ─── Team Comparison ───
    st.markdown('<div class="section-title">🏢 Team Average Predicted Position</div>', unsafe_allow_html=True)
    team_avg = predictions.groupby("Team")["PredictedPosition"].mean().sort_values()
    fig3 = px.bar(
        x=team_avg.values,
        y=team_avg.index,
        orientation="h",
        color=team_avg.index,
        color_discrete_map=TEAM_COLORS,
        labels={"x": "Average Predicted Position", "y": ""},
    )
    fig3.update_layout(
        showlegend=False,
        yaxis=dict(autorange="reversed"),
        height=400,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e6edf3"),
    )
    st.plotly_chart(fig3, use_container_width=True)


# ---------------------------------------------------------------------------
# Page: Driver Analysis
# ---------------------------------------------------------------------------
def show_driver_analysis(year, gp_name):
    st.markdown(f"""
    <div class="race-header">
        <h1>🔍 Driver Analysis</h1>
        <div class="subtitle">{gp_name} {year}</div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Loading data..."):
        result = predict_race(year, gp_name)

    predictions = result["predictions"]

    driver_options = [
        f"{DRIVER_NAMES.get(d, d)} ({d})" for d in predictions["Driver"]
    ]
    selected = st.selectbox("Select Driver", driver_options)
    driver_code = selected.split("(")[1].strip(")")

    driver_data = predictions[predictions["Driver"] == driver_code].iloc[0]

    # Driver metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Team", driver_data["Team"])
    col2.metric("Predicted Position", f"{driver_data['PredictedPosition']:.1f}")
    col3.metric("Uncertainty", f"±{driver_data['Uncertainty']:.1f}")
    col4.metric("Confidence", f"{driver_data['Confidence']:.0%}")

    # If past race, show actual result
    if result["status"] == "past" and result["actual_results"] is not None:
        actual_row = result["actual_results"][result["actual_results"]["Driver"] == driver_code]
        if not actual_row.empty:
            actual_pos = int(actual_row.iloc[0]["Position"])
            delta = round(driver_data["PredictedPosition"] - actual_pos, 1)
            st.metric("Actual Position", actual_pos, delta=f"{delta:+.1f} vs predicted", delta_color="inverse")

    # Feature radar chart
    feature_cols = [c for c in FEATURE_COLUMNS if c in predictions.columns]
    if feature_cols:
        driver_vals = driver_data[feature_cols].values.astype(float)
        max_vals = predictions[feature_cols].max().values.astype(float)
        max_vals[max_vals == 0] = 1
        normalized = driver_vals / max_vals

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=normalized,
            theta=[c.replace("_", " ").title() for c in feature_cols],
            fill="toself",
            name=DRIVER_NAMES.get(driver_code, driver_code),
            line_color=get_team_color(driver_data["Team"]),
            fillcolor=get_team_color(driver_data["Team"]).replace(")", ",0.2)").replace("rgb", "rgba")
            if get_team_color(driver_data["Team"]).startswith("rgb") else get_team_color(driver_data["Team"]) + "33",
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1]),
                bgcolor="rgba(0,0,0,0)",
            ),
            title=f"Feature Profile: {DRIVER_NAMES.get(driver_code, driver_code)}",
            height=500,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e6edf3"),
        )
        st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------------------------
# Page: Model Training
# ---------------------------------------------------------------------------
def show_training():
    st.markdown("""
    <div class="race-header">
        <h1>🔧 Model Training</h1>
        <div class="subtitle">Train the neural network ensemble on historical F1 data</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        n_models = st.slider("Number of models in ensemble", 3, 10, 5)
        epochs = st.slider("Training epochs", 100, 1000, 300)
        lr = st.select_slider(
            "Learning rate",
            options=[0.0001, 0.0005, 0.001, 0.005, 0.01],
            value=0.001,
        )

    if st.button("🚀 Train Model", type="primary"):
        with st.spinner("Training... this may take a minute"):
            from model import F1EnsembleModel
            from data_pipeline import prepare_training_data

            X, y, _ = prepare_training_data()
            m = F1EnsembleModel(n_models=n_models)
            m.train(X, y, epochs=epochs, lr=lr)
            m.save()

            mean_pred, std_pred = m.predict(X)
            mae = np.mean(np.abs(mean_pred - y))
            st.success(f"✅ Training complete! MAE: {mae:.2f} positions")
            st.balloons()


# ---------------------------------------------------------------------------
# Route to the selected page
# ---------------------------------------------------------------------------
if page == "Race Predictions":
    show_predictions(selected_year, selected_gp)
elif page == "Driver Analysis":
    show_driver_analysis(selected_year, selected_gp)
elif page == "Model Training":
    show_training()