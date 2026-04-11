"""Central configuration for the F1 prediction project."""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data_cache")
MODEL_DIR = os.path.join(BASE_DIR, "models")
CACHE_DIR = os.path.join(DATA_DIR, "fastf1_cache")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

# 2026 F1 Driver Lineup (Bahrain GP)
DRIVERS_2026 = {
    "VER": "Red Bull Racing",
    "PER": "Red Bull Racing",
    "NOR": "McLaren",
    "PIA": "McLaren",
    "LEC": "Ferrari",
    "HAM": "Ferrari",
    "RUS": "Mercedes",
    "ANO": "Mercedes",
    "ALO": "Aston Martin",
    "STR": "Aston Martin",
    "GAS": "Alpine",
    "DOO": "Alpine",
    "TSU": "Racing Bulls",
    "LAW": "Racing Bulls",
    "HUL": "Kick Sauber",
    "BOR": "Kick Sauber",
    "SAI": "Williams",
    "ALB": "Williams",
    "OCO": "Haas",
    "BEA": "Haas",
}

TEAM_COLORS = {
    "Red Bull Racing": "#3671C6",
    "McLaren": "#FF8000",
    "Ferrari": "#E8002D",
    "Mercedes": "#27F4D2",
    "Aston Martin": "#229971",
    "Alpine": "#FF87BC",
    "Racing Bulls": "#6692FF",
    "Kick Sauber": "#52E252",
    "Williams": "#64C4FF",
    "Haas": "#B6BABD",
}

# Feature engineering config
FEATURE_COLUMNS = [
    "races_count",
    "avg_position",
    "position_std",
    "avg_points",
    "total_points",
    "podium_rate",
    "top10_rate",
    "position_volatility",
    "avg_grid",
    "grid_to_finish_delta",
    "bahrain_avg_position",
    "bahrain_races_count",
]

PREDICTIONS_CSV = os.path.join(BASE_DIR, "bahrain_predictions_2026.csv")