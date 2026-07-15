"""Backward-compatible prediction wrapper.

Delegates to race_predictor.py for the actual prediction logic.
Kept for backward compatibility with existing scripts that import from predict.py.
"""
import os
import numpy as np
import pandas as pd
from config import DRIVERS_2026, PREDICTIONS_CSV, FEATURE_COLUMNS, TEAM_COLORS
from race_predictor import predict_race, get_team_color


def predict_bahrain(model=None):
    """Generate Bahrain GP 2026 predictions (backward-compatible wrapper)."""
    result = predict_race(2026, "Bahrain Grand Prix", model=model)
    predictions = result["predictions"]

    # Print results
    print_results(predictions)

    # Save CSV
    save_df = predictions.copy()
    for col in save_df.columns:
        if save_df[col].dtype != object:
            save_df[col] = save_df[col].apply(
                lambda x: round(float(x), 3)
                if isinstance(x, (int, float, np.integer, np.floating)) else x
            )
    save_df.to_csv(PREDICTIONS_CSV)
    print(f"\nPredictions saved to {PREDICTIONS_CSV}")
    return predictions


def print_results(results):
    """Print a formatted prediction table."""
    print("\n" + "=" * 78)
    print("  F1 RACE PREDICTIONS")
    print("=" * 78)
    print(f"{'#':>3} {'Driver':<6} {'Team':<20} {'Pred Pos':>8} {'+/-':>6} {'Conf':>6}")
    print("-" * 78)

    for idx, row in results.iterrows():
        uncertainty = row["Uncertainty"]
        confidence = row["Confidence"]
        team = row["Team"]
        driver = row["Driver"]
        pred_pos = row["PredictedPosition"]

        conf_bar = ">" * int(confidence * 10)
        print(f"{idx:>3}  {driver:<6} {team:<20} {pred_pos:>8.1f} {uncertainty:>+6.1f} {conf_bar:<10} {confidence:.0%}")

    print("=" * 78)
    print(f"  Top 3 predicted: {', '.join(results.head(3)['Driver'].tolist())}")
    print(f"  Confidence range: {results['Confidence'].min():.0%} - {results['Confidence'].max():.0%}")
    print("=" * 78)


if __name__ == "__main__":
    predict_bahrain()