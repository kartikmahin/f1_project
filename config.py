"""Central configuration for the F1 prediction project."""
import os
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data_cache")
MODEL_DIR = os.path.join(BASE_DIR, "models")
CACHE_DIR = os.path.join(DATA_DIR, "fastf1_cache")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# 2026 F1 Driver Lineup
# ---------------------------------------------------------------------------
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

# Full driver name mapping (abbreviation -> full name)
DRIVER_NAMES = {
    "VER": "Max Verstappen",
    "PER": "Sergio Perez",
    "NOR": "Lando Norris",
    "PIA": "Oscar Piastri",
    "LEC": "Charles Leclerc",
    "HAM": "Lewis Hamilton",
    "RUS": "George Russell",
    "ANO": "Kimi Antonelli",
    "ALO": "Fernando Alonso",
    "STR": "Lance Stroll",
    "GAS": "Pierre Gasly",
    "DOO": "Jack Doohan",
    "TSU": "Yuki Tsunoda",
    "LAW": "Liam Lawson",
    "HUL": "Nico Hulkenberg",
    "BOR": "Gabriel Bortoleto",
    "SAI": "Carlos Sainz",
    "ALB": "Alexander Albon",
    "OCO": "Esteban Ocon",
    "BEA": "Oliver Bearman",
    # Legacy drivers (for historical data)
    "BOT": "Valtteri Bottas",
    "ZHO": "Guanyu Zhou",
    "MAG": "Kevin Magnussen",
    "RIC": "Daniel Ricciardo",
    "SAR": "Logan Sargeant",
    "DEV": "Nyck de Vries",
    "KVY": "Daniil Kvyat",
    "COL": "Franco Colapinto",
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
    # Legacy team names
    "AlphaTauri": "#6692FF",
    "Alfa Romeo": "#52E252",
}

# ---------------------------------------------------------------------------
# F1 Calendar — used to determine past vs future races
# Dates are approximate race-day dates.
# ---------------------------------------------------------------------------
F1_CALENDAR = {
    2024: {
        "Bahrain Grand Prix":           date(2024, 3, 2),
        "Saudi Arabian Grand Prix":     date(2024, 3, 9),
        "Australian Grand Prix":        date(2024, 3, 24),
        "Japanese Grand Prix":          date(2024, 4, 7),
        "Chinese Grand Prix":           date(2024, 4, 21),
        "Miami Grand Prix":             date(2024, 5, 5),
        "Emilia Romagna Grand Prix":    date(2024, 5, 19),
        "Monaco Grand Prix":            date(2024, 5, 26),
        "Canadian Grand Prix":          date(2024, 6, 9),
        "Spanish Grand Prix":           date(2024, 6, 23),
        "Austrian Grand Prix":          date(2024, 6, 30),
        "British Grand Prix":           date(2024, 7, 7),
        "Hungarian Grand Prix":         date(2024, 7, 21),
        "Belgian Grand Prix":           date(2024, 7, 28),
        "Dutch Grand Prix":             date(2024, 8, 25),
        "Italian Grand Prix":           date(2024, 9, 1),
        "Azerbaijan Grand Prix":        date(2024, 9, 15),
        "Singapore Grand Prix":         date(2024, 9, 22),
        "United States Grand Prix":     date(2024, 10, 20),
        "Mexico City Grand Prix":       date(2024, 10, 27),
        "São Paulo Grand Prix":         date(2024, 11, 3),
        "Las Vegas Grand Prix":         date(2024, 11, 23),
        "Qatar Grand Prix":             date(2024, 12, 1),
        "Abu Dhabi Grand Prix":         date(2024, 12, 8),
    },
    2025: {
        "Australian Grand Prix":        date(2025, 3, 16),
        "Chinese Grand Prix":           date(2025, 3, 23),
        "Japanese Grand Prix":          date(2025, 4, 6),
        "Bahrain Grand Prix":           date(2025, 4, 13),
        "Saudi Arabian Grand Prix":     date(2025, 4, 20),
        "Miami Grand Prix":             date(2025, 5, 4),
        "Emilia Romagna Grand Prix":    date(2025, 5, 18),
        "Monaco Grand Prix":            date(2025, 5, 25),
        "Spanish Grand Prix":           date(2025, 6, 1),
        "Canadian Grand Prix":          date(2025, 6, 15),
        "Austrian Grand Prix":          date(2025, 6, 29),
        "British Grand Prix":           date(2025, 7, 6),
        "Belgian Grand Prix":           date(2025, 7, 27),
        "Hungarian Grand Prix":         date(2025, 7, 20),
        "Dutch Grand Prix":             date(2025, 8, 31),
        "Italian Grand Prix":           date(2025, 9, 7),
        "Azerbaijan Grand Prix":        date(2025, 9, 21),
        "Singapore Grand Prix":         date(2025, 10, 5),
        "United States Grand Prix":     date(2025, 10, 19),
        "Mexico City Grand Prix":       date(2025, 10, 26),
        "São Paulo Grand Prix":         date(2025, 11, 9),
        "Las Vegas Grand Prix":         date(2025, 11, 22),
        "Qatar Grand Prix":             date(2025, 11, 30),
        "Abu Dhabi Grand Prix":         date(2025, 12, 7),
    },
    2026: {
        "Australian Grand Prix":        date(2026, 3, 15),
        "Chinese Grand Prix":           date(2026, 3, 29),
        "Japanese Grand Prix":          date(2026, 4, 5),
        "Bahrain Grand Prix":           date(2026, 4, 19),
        "Saudi Arabian Grand Prix":     date(2026, 4, 26),
        "Miami Grand Prix":             date(2026, 5, 10),
        "Emilia Romagna Grand Prix":    date(2026, 5, 24),
        "Monaco Grand Prix":            date(2026, 5, 31),
        "Spanish Grand Prix":           date(2026, 6, 14),
        "Canadian Grand Prix":          date(2026, 6, 28),
        "Austrian Grand Prix":          date(2026, 7, 5),
        "British Grand Prix":           date(2026, 7, 19),
        "Hungarian Grand Prix":         date(2026, 7, 26),
        "Belgian Grand Prix":           date(2026, 8, 2),
        "Dutch Grand Prix":             date(2026, 8, 30),
        "Italian Grand Prix":           date(2026, 9, 6),
        "Azerbaijan Grand Prix":        date(2026, 9, 20),
        "Singapore Grand Prix":         date(2026, 10, 4),
        "United States Grand Prix":     date(2026, 10, 18),
        "Mexico City Grand Prix":       date(2026, 10, 25),
        "São Paulo Grand Prix":         date(2026, 11, 8),
        "Las Vegas Grand Prix":         date(2026, 11, 22),
        "Qatar Grand Prix":             date(2026, 11, 29),
        "Abu Dhabi Grand Prix":         date(2026, 12, 6),
    },
}


def is_race_in_past(year: int, gp_name: str) -> bool:
    """Check if a race has already happened based on today's date."""
    today = date.today()
    calendar = F1_CALENDAR.get(year, {})
    race_date = calendar.get(gp_name)
    if race_date is None:
        # If we don't have the date, assume past for years before current
        return year < today.year
    return race_date < today


def get_race_date(year: int, gp_name: str):
    """Return the race date or None."""
    return F1_CALENDAR.get(year, {}).get(gp_name)


def get_gp_list(year: int):
    """Return list of GP names for a given year, in calendar order."""
    calendar = F1_CALENDAR.get(year, {})
    return sorted(calendar.keys(), key=lambda gp: calendar[gp])


# ---------------------------------------------------------------------------
# Feature engineering config (generic — works for any track)
# ---------------------------------------------------------------------------
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
    "track_avg_position",     # replaces bahrain_avg_position
    "track_races_count",      # replaces bahrain_races_count
]

PREDICTIONS_CSV = os.path.join(BASE_DIR, "predictions.csv")