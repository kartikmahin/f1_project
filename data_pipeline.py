"""Data collection and preprocessing pipeline for F1 predictions.

Supports any Grand Prix track — not just Bahrain.
"""
import os
import fastf1
import pandas as pd
import numpy as np
from config import DATA_DIR, CACHE_DIR, DRIVERS_2026

fastf1.Cache.enable_cache(CACHE_DIR)


def collect_race_data(years=None, gp_list=None):
    """Collect race and qualifying results from FastF1."""
    if years is None:
        years = [2024, 2025]

    all_results = []
    for year in years:
        schedule = fastf1.get_event_schedule(year)
        races = gp_list or schedule["EventName"].tolist()

        for gp in races:
            if pd.isna(gp):
                continue
            for session_type in ["R", "Q"]:
                try:
                    session = fastf1.get_session(year, gp, session_type)
                    session.load()
                    results = session.results
                    if results is not None and not results.empty:
                        results["GrandPrix"] = gp
                        results["Year"] = year
                        results["SessionType"] = "Race" if session_type == "R" else "Qualifying"
                        all_results.append(results)
                        print(f"  Loaded: {gp} {year} ({'Race' if session_type == 'R' else 'Qual'})")
                except Exception as e:
                    print(f"  Skip {gp} {year} {session_type}: {e}")

    if not all_results:
        return pd.DataFrame()

    df = pd.concat(all_results, ignore_index=True)
    path = os.path.join(DATA_DIR, "all_race_results.csv")
    df.to_csv(path, index=False)
    print(f"Saved {len(df)} records to {path}")
    return df


def create_sample_data():
    """Generate realistic synthetic F1 data for training when live data is unavailable."""
    np.random.seed(42)
    drivers = list(DRIVERS_2026.keys())
    teams = DRIVERS_2026

    # Base performance tiers (lower = better)
    performance = {
        "VER": 1.0, "NOR": 2.0, "LEC": 2.5, "HAM": 3.0, "RUS": 3.5,
        "PIA": 4.0, "ANO": 5.0, "ALO": 6.0, "SAI": 4.5, "GAS": 7.5,
        "PER": 5.5, "STR": 8.5, "TSU": 7.0, "LAW": 7.5, "HUL": 9.0,
        "ALB": 8.0, "OCO": 8.0, "DOO": 9.5, "BOR": 10.0, "BEA": 9.5,
    }

    data = []
    years = [2024, 2025]
    gps = [
        "Bahrain Grand Prix", "Saudi Arabian Grand Prix", "Australian Grand Prix",
        "Japanese Grand Prix", "Chinese Grand Prix", "Miami Grand Prix",
        "Monaco Grand Prix", "Canadian Grand Prix", "Spanish Grand Prix",
        "British Grand Prix", "Austrian Grand Prix", "Belgian Grand Prix",
        "Dutch Grand Prix", "Italian Grand Prix", "Singapore Grand Prix",
        "Azerbaijan Grand Prix", "United States Grand Prix", "Mexico City Grand Prix",
        "São Paulo Grand Prix", "Abu Dhabi Grand Prix",
        "Emilia Romagna Grand Prix", "Hungarian Grand Prix", "Las Vegas Grand Prix",
        "Qatar Grand Prix",
    ]

    for year in years:
        for gp in gps:
            base_perf = {}
            for d in drivers:
                # Add randomness around base performance
                noise = np.random.normal(0, 2.5)
                # Track-specific bonus: some drivers excel at certain tracks
                track_bonus = 0
                track_hash = hash(gp + d) % 10
                if track_hash < 3:
                    track_bonus = np.random.normal(-0.5, 0.5)
                elif track_hash > 7:
                    track_bonus = np.random.normal(0.3, 0.5)
                base_perf[d] = performance[d] + noise + track_bonus

            sorted_drivers = sorted(base_perf.items(), key=lambda x: x[1])
            for pos, (driver, score) in enumerate(sorted_drivers, 1):
                grid = max(1, pos + np.random.randint(-3, 4))
                points = max(0, 25 - (pos - 1) * 2) if pos <= 10 else 0
                # DNF probability ~5% for midfield, ~2% for top teams
                dnf_prob = 0.05 if performance[driver] > 6 else 0.02
                status = "Finished" if np.random.random() > dnf_prob else "DNF"

                data.append({
                    "Driver": driver,
                    "Team": teams[driver],
                    "Position": pos,
                    "GridPosition": grid,
                    "Points": points,
                    "Status": status,
                    "GrandPrix": gp,
                    "Year": year,
                })

    df = pd.DataFrame(data)
    path = os.path.join(DATA_DIR, "all_race_results.csv")
    df.to_csv(path, index=False)
    print(f"Created sample data: {len(df)} records -> {path}")
    return df


def engineer_features(df, target_gp=None, target_drivers=None):
    """Build feature matrix from historical race data.

    Args:
        df: Historical race results DataFrame.
        target_gp: The GP name to compute track-specific features for.
                    If None, track features default to overall averages.
        target_drivers: List of driver abbreviations. Defaults to DRIVERS_2026.
    """
    if target_drivers is None:
        target_drivers = list(DRIVERS_2026.keys())

    df = df.sort_values(["Year", "GrandPrix", "Position"])
    features_list = []

    for driver in target_drivers:
        driver_df = df[df["Driver"] == driver].copy()
        if len(driver_df) == 0:
            continue

        driver_df = driver_df.sort_values(["Year", "GrandPrix"])

        # Career stats
        total_races = len(driver_df)
        avg_pos = driver_df["Position"].mean()
        pos_std = driver_df["Position"].std() if total_races > 1 else 0
        avg_points = driver_df["Points"].mean()
        total_points = driver_df["Points"].sum()
        podium_rate = (driver_df["Position"] <= 3).sum() / max(total_races, 1)
        top10_rate = (driver_df["Position"] <= 10).sum() / max(total_races, 1)

        # Recent form (last 5 races)
        recent = driver_df.tail(5)
        recent_avg_pos = recent["Position"].mean()
        recent_std = recent["Position"].std() if len(recent) > 1 else 0
        recent_points = recent["Points"].sum()

        # Grid vs finish delta (overtaking ability)
        avg_grid = driver_df["GridPosition"].mean()
        grid_delta = avg_grid - avg_pos  # positive = gains positions

        # Position volatility (consistency measure)
        volatility = abs(driver_df["Position"].diff()).mean() if total_races > 1 else 0

        # Track-specific performance (generic — works for any GP)
        if target_gp:
            track_df = driver_df[driver_df["GrandPrix"].str.contains(
                target_gp.replace("Grand Prix", "").strip(), na=False, case=False
            )]
        else:
            track_df = pd.DataFrame()

        track_avg = track_df["Position"].mean() if len(track_df) > 0 else avg_pos
        track_count = len(track_df)

        # Trend (improving or declining)
        if total_races >= 4:
            first_half = driver_df.iloc[: total_races // 2]["Position"].mean()
            second_half = driver_df.iloc[total_races // 2 :]["Position"].mean()
            trend = first_half - second_half  # positive = improving
        else:
            trend = 0

        features_list.append({
            "Driver": driver,
            "Team": DRIVERS_2026.get(driver, "Unknown"),
            "races_count": total_races,
            "avg_position": round(float(avg_pos), 2),
            "position_std": round(float(pos_std), 2),
            "avg_points": round(float(avg_points), 2),
            "total_points": round(float(total_points), 1),
            "podium_rate": round(float(podium_rate), 3),
            "top10_rate": round(float(top10_rate), 3),
            "position_volatility": round(float(volatility), 2),
            "avg_grid": round(float(avg_grid), 2),
            "grid_to_finish_delta": round(float(grid_delta), 2),
            "track_avg_position": round(float(track_avg), 2),
            "track_races_count": track_count,
            "recent_avg_pos": round(float(recent_avg_pos), 2),
            "recent_points": round(float(recent_points), 1),
            "recent_std": round(float(recent_std), 2),
            "trend": round(float(trend), 2),
            # Target: track-specific avg position (what we predict)
            "target": round(float(track_avg), 2) if track_count > 0 else round(float(avg_pos), 2),
        })

    return pd.DataFrame(features_list)


def prepare_training_data(df=None, target_gp=None):
    """Load data and prepare feature matrix for training.

    Args:
        df: Optional pre-loaded DataFrame.
        target_gp: GP name for track-specific features.
    """
    if df is None:
        path = os.path.join(DATA_DIR, "all_race_results.csv")
        if not os.path.exists(path):
            print("No data found, generating sample data...")
            df = create_sample_data()
        else:
            df = pd.read_csv(path)

    features_df = engineer_features(df, target_gp=target_gp)

    from config import FEATURE_COLUMNS
    X = features_df[FEATURE_COLUMNS].values.astype(np.float32)
    y = features_df["target"].values.astype(np.float32)

    return X, y, features_df