"""Streamlit dashboard for F1 Bahrain Grand Prix 2026 predictions.

Run with: streamlit run dashboard.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go

from config import DRIVERS_2026, TEAM_COLORS, FEATURE_COLUMNS, PREDICTIONS_CSV, BASE_DIR
from predict import predict_bahrain, get_team_color


def run_dashboard():
    st.set_page_config(
        page_title="F1 Bahrain GP 2026 Predictor",
        page_icon=":race_car:",
        layout="wide",
    )

    # --- Sidebar ---
    st.sidebar.title(":race_car: F1 Predictor")
    st.sidebar.markdown("**Bahrain Grand Prix 2026**")
    st.sidebar.markdown("---")

    action = st.sidebar.radio("Action", ["View Predictions", "Retrain Model", "Driver Analysis"])

    # --- Main Content ---
    st.title(":checkered_flag: Bahrain Grand Prix 2026 - Race Predictions")
    st.markdown("Neural network ensemble model trained on historical F1 race data with uncertainty estimation.")

    if action == "View Predictions":
        show_predictions()
    elif action == "Retrain Model":
        show_training()
    elif action == "Driver Analysis":
        show_driver_analysis()


def show_predictions():
    results = predict_bahrain()

    # --- Podium Section ---
    st.markdown("## :trophy: Predicted Podium")
    podium = results.head(3)
    cols = st.columns(3)
    positions = ["1st", "2nd", "3rd"]
    emojis = [":first_place_medal:", ":second_place_medal:", ":third_place_medal:"]
    for i, col in enumerate(cols):
        if i < len(podium):
            row = podium.iloc[i]
            driver = row["Driver"]
            team = row["Team"]
            conf = row["Confidence"]
            team_color = get_team_color(team)
            col.markdown(f"### {emojis[i]} {positions[i]}")
            col.markdown(f"**{driver}**")
            col.markdown(f"{team}")
            col.progress(min(float(conf), 1.0))

    st.markdown("---")

    # --- Full Grid ---
    st.markdown("## :chart_with_bars: Predicted Grid Order")
    display_df = results[["Driver", "Team", "PredictedPosition", "Uncertainty", "Confidence"]].copy()
    display_df.columns = ["Driver", "Team", "Predicted Position", "Uncertainty (+/-)", "Confidence"]
    display_df["Predicted Position"] = display_df["Predicted Position"].round(1)
    display_df["Uncertainty (+/-)"] = display_df["Uncertainty (+/-)"].round(1)
    display_df["Confidence"] = display_df["Confidence"].apply(lambda x: f"{x:.0%}")
    st.dataframe(display_df, use_container_width=True)

    # --- Position Chart ---
    st.markdown("## :bar_chart: Predicted Positions with Uncertainty")
    fig = go.Figure()
    for idx, row in results.iterrows():
        team_color = get_team_color(row["Team"])
        fig.add_trace(go.Bar(
            name=row["Driver"],
            x=[row["Driver"]],
            y=[row["PredictedPosition"]],
            error_y=dict(type="data", array=[row["Uncertainty"]], visible=True),
            marker_color=team_color,
            hovertext=f"{row['Team']}<br>Confidence: {row['Confidence']:.0%}",
        ))
    fig.update_layout(
        title="Predicted Finish Positions (lower = better)",
        yaxis_title="Predicted Position",
        xaxis_title="Driver",
        showlegend=False,
        height=500,
        yaxis=dict(autorange="reversed"),
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Team Comparison ---
    st.markdown("## :team: Team Average Predicted Position")
    team_avg = results.groupby("Team")["PredictedPosition"].mean().sort_values()
    fig2 = px.bar(
        x=team_avg.values,
        y=team_avg.index,
        orientation="h",
        color=team_avg.index,
        color_discrete_map=TEAM_COLORS,
        title="Average Predicted Position by Team",
        labels={"x": "Average Predicted Position", "y": ""},
    )
    fig2.update_layout(showlegend=False, yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig2, use_container_width=True)


def show_training():
    st.markdown("## :wrench: Model Training")
    st.markdown("Train the neural network ensemble model on historical F1 data.")

    col1, col2 = st.columns(2)
    with col1:
        n_models = st.slider("Number of models in ensemble", 3, 10, 5)
        epochs = st.slider("Training epochs", 100, 1000, 300)
        lr = st.select_slider("Learning rate", options=[0.0001, 0.0005, 0.001, 0.005, 0.01], value=0.001)

    if st.button("Train Model", type="primary"):
        with st.spinner("Training... this may take a minute"):
            from model import train_model
            from data_pipeline import prepare_training_data
            X, y, _ = prepare_training_data()
            from model import F1EnsembleModel
            m = F1EnsembleModel(n_models=n_models)
            m.train(X, y, epochs=epochs, lr=lr)
            m.save()

            mean_pred, std_pred = m.predict(X)
            mae = np.mean(np.abs(mean_pred - y))
            st.success(f"Training complete! MAE: {mae:.2f} positions")
            st.balloons()


def show_driver_analysis():
    results = predict_bahrain()

    st.markdown("## :mag: Driver Deep Dive")

    driver = st.selectbox("Select Driver", results["Driver"].tolist())
    driver_data = results[results["Driver"] == driver].iloc[0]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Team", driver_data["Team"])
    col2.metric("Predicted Position", f"{driver_data['PredictedPosition']:.1f}")
    col3.metric("Uncertainty", f"+/- {driver_data['Uncertainty']:.1f}")
    col4.metric("Confidence", f"{driver_data['Confidence']:.0%}")

    # Feature radar chart
    feature_cols = [c for c in FEATURE_COLUMNS if c in results.columns]
    if feature_cols:
        driver_vals = driver_data[feature_cols].values.astype(float)
        # Normalize to 0-1 for radar chart
        max_vals = results[feature_cols].max().values.astype(float)
        max_vals[max_vals == 0] = 1
        normalized = driver_vals / max_vals

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=normalized,
            theta=feature_cols,
            fill="toself",
            name=driver,
            line_color=get_team_color(driver_data["Team"]),
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            title=f"Feature Profile: {driver}",
            height=500,
        )
        st.plotly_chart(fig, use_container_width=True)

    # Comparison table
    st.markdown("### Feature Comparison")
    comp_df = results[["Driver", "Team"] + feature_cols].copy()
    comp_df = comp_df.sort_values("PredictedPosition") if "PredictedPosition" in results.columns else comp_df
    for col in feature_cols:
        if col in comp_df.columns:
            comp_df[col] = comp_df[col].astype(float).round(2)
    st.dataframe(comp_df, use_container_width=True)


if __name__ == "__main__":
    run_dashboard()