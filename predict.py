"""Prediction engine for the Bahrain Grand Prix 2026."""
import os
import numpy as np
import pandas as pd
from config import DRIVERS_2026, PREDICTIONS_CSV, FEATURE_COLUMNS, TEAM_COLORS
from data_pipeline import prepare_training_data, create_sample_data


def predict_bahrain(model=None):
    """Generate Bahrain GP 2026 predictions using the trained ensemble model."""
    # Load or prepare data
    X, y, features_df = prepare_training_data()

    # Load or train model
    model_path = os.path.join(os.path.dirname(__file__), "models", "f1_ensemble.pth")
    if model is None:
        from model import F1EnsembleModel
        model = F1EnsembleModel()
        if os.path.exists(model_path):
            model.load(model_path)
        else:
            print("No trained model found, training...")
            model.train(X, y)

    # Generate predictions with uncertainty
    mean_pred, std_pred = model.predict(X)

    # Build results DataFrame
    results = features_df[["Driver", "Team"]].copy()
    results["PredictedPosition"] = np.clip(mean_pred, 1, 20)
    results["Uncertainty"] = np.clip(std_pred, 0.5, 5.0)
    results["Confidence"] = np.clip(1.0 - (std_pred / 5.0), 0.1, 0.99)

    # Add readable features
    for col in FEATURE_COLUMNS:
        if col in features_df.columns:
            results[col] = features_df[col].values

    # Sort by predicted position
    results = results.sort_values("PredictedPosition").reset_index(drop=True)
    results.index = results.index + 1
    results.index.name = "PredictedFinish"

    # Print nice results
    print_results(results)

    # Save clean CSV (no numpy type junk)
    save_df = results.copy()
    for col in save_df.columns:
        if save_df[col].dtype == object:
            pass
        else:
            save_df[col] = save_df[col].apply(lambda x: round(float(x), 3) if isinstance(x, (int, float, np.integer, np.floating)) else x)
    save_df.to_csv(PREDICTIONS_CSV)
    print(f"\nPredictions saved to {PREDICTIONS_CSV}")

    return results


def print_results(results):
    """Print a formatted prediction table."""
    print("\n" + "=" * 78)
    print("  BAHRAIN GRAND PRIX 2026 - PREDICTED STANDINGS")
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


def get_team_color(team):
    return TEAM_COLORS.get(team, "#888888")


if __name__ == "__main__":
    predict_bahrain()