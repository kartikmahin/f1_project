"""Universal F1 Race Predictor — works for any GP, past or future.

For past races: returns real results + predicted results + comparison.
For future races: returns predicted results only with a "not happened yet" flag.
"""
import os
import numpy as np
import pandas as pd
import fastf1

from config import (
    DRIVERS_2026, DRIVER_NAMES, TEAM_COLORS, FEATURE_COLUMNS,
    PREDICTIONS_CSV, DATA_DIR, CACHE_DIR,
    is_race_in_past, get_race_date, get_gp_list, F1_CALENDAR,
)
from data_pipeline import prepare_training_data, create_sample_data

fastf1.Cache.enable_cache(CACHE_DIR)


def get_actual_results(year: int, gp_name: str) -> pd.DataFrame | None:
    """Fetch actual race results from FastF1 for a past race.

    Returns a DataFrame with columns [Position, Driver, Team, Points, Status]
    or None if the data cannot be loaded.
    """
    try:
        session = fastf1.get_session(year, gp_name, "R")
        session.load()
        results = session.results
        if results is None or results.empty:
            return None

        # Normalize the results
        df = pd.DataFrame()
        df["Position"] = pd.to_numeric(results["Position"], errors="coerce")
        df["Driver"] = results["Abbreviation"].values
        df["DriverFullName"] = results["FullName"].values if "FullName" in results.columns else results["Abbreviation"].values
        df["Team"] = results["TeamName"].values
        df["Points"] = pd.to_numeric(results["Points"], errors="coerce").fillna(0)
        df["Status"] = results["Status"].values if "Status" in results.columns else "Finished"
        df["GridPosition"] = pd.to_numeric(results["GridPosition"], errors="coerce").fillna(20)

        df = df.dropna(subset=["Position"]).sort_values("Position").reset_index(drop=True)
        df["Position"] = df["Position"].astype(int)
        return df

    except Exception as e:
        print(f"Could not load actual results for {gp_name} {year}: {e}")

    # Fallback: try cached CSV data
    try:
        csv_path = os.path.join(DATA_DIR, "all_race_results.csv")
        if os.path.exists(csv_path):
            all_data = pd.read_csv(csv_path)
            race_data = all_data[
                (all_data["Year"] == year) &
                (all_data["GrandPrix"].str.contains(
                    gp_name.replace("Grand Prix", "").strip(), na=False, case=False
                ))
            ]
            if not race_data.empty:
                df = race_data[["Position", "Driver", "Team", "Points"]].copy()
                df["Status"] = race_data.get("Status", "Finished")
                df["GridPosition"] = race_data.get("GridPosition", 20)
                df["DriverFullName"] = df["Driver"].map(
                    lambda x: DRIVER_NAMES.get(x, x)
                )
                df["Position"] = pd.to_numeric(df["Position"], errors="coerce")
                df = df.dropna(subset=["Position"]).sort_values("Position").reset_index(drop=True)
                df["Position"] = df["Position"].astype(int)
                return df
    except Exception:
        pass

    return None


def generate_predictions(year: int, gp_name: str, model=None):
    """Generate predicted race positions for any GP.

    Returns a DataFrame with columns:
        [Driver, Team, PredictedPosition, Uncertainty, Confidence, ...]
    """
    # Prepare data with track-specific features
    X, y, features_df = prepare_training_data(target_gp=gp_name)

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
            model.save()

    # Generate predictions with uncertainty
    mean_pred, std_pred = model.predict(X)

    # Build results DataFrame
    results = features_df[["Driver", "Team"]].copy()
    results["PredictedPosition"] = np.clip(mean_pred, 1, 20)
    results["Uncertainty"] = np.clip(std_pred, 0.5, 5.0)
    results["Confidence"] = np.clip(1.0 - (std_pred / 5.0), 0.1, 0.99)
    results["DriverFullName"] = results["Driver"].map(
        lambda x: DRIVER_NAMES.get(x, x)
    )

    # Add readable features
    for col in FEATURE_COLUMNS:
        if col in features_df.columns:
            results[col] = features_df[col].values

    # Sort by predicted position
    results = results.sort_values("PredictedPosition").reset_index(drop=True)
    results.index = results.index + 1
    results.index.name = "PredictedFinish"

    return results


def predict_race(year: int, gp_name: str, model=None) -> dict:
    """Main entry point — predict a race and determine if it's past or future.

    Returns:
        {
            "year": int,
            "gp_name": str,
            "race_date": date | None,
            "status": "past" | "future",
            "predictions": DataFrame,
            "actual_results": DataFrame | None,
            "comparison": DataFrame | None,
            "accuracy": dict | None,
        }
    """
    race_date = get_race_date(year, gp_name)
    past = is_race_in_past(year, gp_name)

    # Always generate predictions
    predictions = generate_predictions(year, gp_name, model=model)

    result = {
        "year": year,
        "gp_name": gp_name,
        "race_date": race_date,
        "status": "past" if past else "future",
        "predictions": predictions,
        "actual_results": None,
        "comparison": None,
        "accuracy": None,
    }

    if past:
        actual = get_actual_results(year, gp_name)
        result["actual_results"] = actual

        if actual is not None and not actual.empty:
            # Build comparison table
            comparison = _build_comparison(predictions, actual)
            result["comparison"] = comparison
            result["accuracy"] = _compute_accuracy(comparison)

    return result


def _build_comparison(predictions: pd.DataFrame, actual: pd.DataFrame) -> pd.DataFrame:
    """Merge predicted vs actual results for side-by-side comparison."""
    pred = predictions[["Driver", "Team", "PredictedPosition", "Confidence"]].copy()
    pred = pred.rename(columns={"PredictedPosition": "Predicted"})
    pred["Predicted"] = pred["Predicted"].round(1)

    act = actual[["Driver", "Position"]].copy()
    act = act.rename(columns={"Position": "Actual"})

    merged = pd.merge(pred, act, on="Driver", how="outer")

    # Fill missing: drivers who raced but weren't predicted, or vice versa
    merged["Predicted"] = merged["Predicted"].fillna(20)
    merged["Actual"] = merged["Actual"].fillna(20)
    merged["Confidence"] = merged["Confidence"].fillna(0.5)
    merged["Team"] = merged["Team"].fillna("Unknown")

    # Compute delta
    merged["Delta"] = merged["Predicted"] - merged["Actual"]
    merged["AbsDelta"] = merged["Delta"].abs()

    # Add full names
    merged["DriverFullName"] = merged["Driver"].map(
        lambda x: DRIVER_NAMES.get(x, x)
    )

    merged = merged.sort_values("Actual").reset_index(drop=True)
    merged.index = merged.index + 1
    return merged


def _compute_accuracy(comparison: pd.DataFrame) -> dict:
    """Compute accuracy metrics from the comparison table."""
    mae = comparison["AbsDelta"].mean()
    exact_matches = (comparison["AbsDelta"] < 1.0).sum()
    close_matches = (comparison["AbsDelta"] < 3.0).sum()
    total = len(comparison)

    # Podium accuracy
    pred_podium = set(comparison.nsmallest(3, "Predicted")["Driver"])
    actual_podium = set(comparison.nsmallest(3, "Actual")["Driver"])
    podium_correct = len(pred_podium & actual_podium)

    return {
        "mae": round(float(mae), 2),
        "exact_matches": int(exact_matches),
        "close_matches": int(close_matches),
        "total_drivers": int(total),
        "podium_correct": podium_correct,
        "podium_accuracy": f"{podium_correct}/3",
    }


def get_team_color(team: str) -> str:
    """Get team color hex code."""
    return TEAM_COLORS.get(team, "#888888")


if __name__ == "__main__":
    # Quick test
    import sys
    year = int(sys.argv[1]) if len(sys.argv) > 1 else 2024
    gp = sys.argv[2] if len(sys.argv) > 2 else "Bahrain Grand Prix"

    result = predict_race(year, gp)
    print(f"\n{'='*70}")
    print(f"  {gp} {year} — Status: {result['status'].upper()}")
    print(f"{'='*70}")

    if result["status"] == "future":
        print("  ⚠  This race has NOT happened yet. Showing predictions only.\n")

    print("\n  PREDICTED STANDINGS:")
    for idx, row in result["predictions"].iterrows():
        print(f"  {idx:>3}. {row['Driver']:<5} ({row['Team']:<20}) "
              f"Pos: {row['PredictedPosition']:>5.1f}  Conf: {row['Confidence']:.0%}")

    if result["actual_results"] is not None:
        print(f"\n  ACTUAL STANDINGS:")
        for _, row in result["actual_results"].iterrows():
            print(f"  {int(row['Position']):>3}. {row['Driver']:<5} ({row['Team']:<20})")

    if result["accuracy"]:
        acc = result["accuracy"]
        print(f"\n  ACCURACY: MAE={acc['mae']:.2f} | "
              f"Close (<3 pos): {acc['close_matches']}/{acc['total_drivers']} | "
              f"Podium: {acc['podium_accuracy']}")
