import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pickle

DATA_DIR = r"C:\Users\KARTIK MAHIDRAKAR\OneDrive\Desktop\python_ai\f1_project\data_cache"

def load_cached_data():
    race_2024 = pd.read_csv(f"{DATA_DIR}/race_results_2024.csv")
    race_2025 = pd.read_csv(f"{DATA_DIR}/race_results_2025.csv")
    qual_2024 = pd.read_csv(f"{DATA_DIR}/qualifying_results_2024.csv")
    qual_2025 = pd.read_csv(f"{DATA_DIR}/qualifying_results_2025.csv")
    stats_2024 = pd.read_csv(f"{DATA_DIR}/driver_stats_2024.csv")
    stats_2025 = pd.read_csv(f"{DATA_DIR}/driver_stats_2025.csv")
    return race_2024, race_2025, qual_2024, qual_2025, stats_2024, stats_2025

def clean_race_results(df):
    cols_to_keep = ['DriverNumber', 'Driver', 'Team', 'Position', 'GridPosition', 
                    'Time', 'Status', 'Points', 'GrandPrix', 'Year']
    df = df[[c for c in cols_to_keep if c in df.columns]]
    df['Position'] = pd.to_numeric(df['Position'], errors='coerce')
    df['GridPosition'] = pd.to_numeric(df['GridPosition'], errors='coerce')
    df['Points'] = pd.to_numeric(df['Points'], errors='coerce')
    return df.dropna(subset=['Position', 'Driver'])

def clean_qualifying_results(df):
    cols_to_keep = ['DriverNumber', 'Driver', 'Team', 'Position', 'Q1', 'Q2', 'Q3', 'GrandPrix', 'Year']
    df = df[[c for c in cols_to_keep if c in df.columns]]
    df['Position'] = pd.to_numeric(df['Position'], errors='coerce')
    return df.dropna(subset=['Position', 'Driver'])

def process_lap_time(time_str):
    if pd.isna(time_str) or time_str == '\\N':
        return np.nan
    try:
        parts = str(time_str).split(':')
        if len(parts) == 2:
            return float(parts[0]) * 60 + float(parts[1])
        elif len(parts) == 3:
            return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
        return float(time_str)
    except:
        return np.nan

def create_driver_team_encoding(race_df):
    all_drivers = set(race_df['Driver'].unique())
    all_teams = set(race_df['Team'].unique())
    return all_drivers, all_teams

def create_cumulative_features(df, drivers):
    df = df.sort_values(['Year', 'GrandPrix'])
    
    driver_features = {}
    for driver in drivers:
        driver_data = df[df['Driver'] == driver].sort_values('GrandPrix')
        
        positions = driver_data['Position'].tolist()
        grids = driver_data['GridPosition'].tolist()
        
        features = {
            'prev_positions': [],
            'prev_grids': [],
            'avg_position': [],
            'avg_grid': [],
            'position_change': [],
        }
        
        for i in range(len(positions)):
            prev_pos = positions[max(0, i-3):i] if i > 0 else []
            prev_grid = grids[max(0, i-3):i] if i > 0 else []
            
            features['prev_positions'].append(prev_pos)
            features['prev_grids'].append(prev_grid)
            features['avg_position'].append(np.mean(prev_pos) if prev_pos else 10.0)
            features['avg_grid'].append(np.mean(prev_grid) if prev_grid else 10.0)
            features['position_change'].append(
                prev_pos[0] - positions[i] if prev_pos else 0
            )
        
        for key, val in features.items():
            driver_features[f'{driver}_{key}'] = val
    
    return driver_features

def create_sequences(race_df, qual_df, stats_df, n_races=5):
    race_df = race_df.sort_values(['Year', 'GrandPrix'])
    unique_gps = race_df['GrandPrix'].unique()
    
    X, y = [], []
    driver_enc = LabelEncoder()
    team_enc = LabelEncoder()
    
    all_drivers = list(race_df['Driver'].unique())
    all_teams = list(race_df['Team'].unique())
    driver_enc.fit(all_drivers)
    team_enc.fit(all_teams)
    
    print(f"Unique drivers: {len(all_drivers)}, Unique teams: {len(all_teams)}")
    
    for i in range(n_races, len(unique_gps)):
        gp_name = unique_gps[i]
        prev_gps = unique_gps[max(0, i-n_races):i]
        
        gp_races = race_df[race_df['GrandPrix'].isin(prev_gps)]
        
        if gp_races.empty:
            continue
            
        for _, driver_row in gp_races.groupby('Driver'):
            if len(driver_row) < n_races:
                continue
                
            driver = driver_row['Driver'].iloc[-1]
            team = driver_row['Team'].iloc[-1]
            
            features = [
                driver_enc.transform([driver])[0],
                team_enc.transform([team])[0],
                driver_row['Position'].mean(),
                driver_row['GridPosition'].mean(),
                driver_row['Position'].iloc[-1],
                driver_row['Position'].iloc[-2] if len(driver_row) > 1 else 10,
                driver_row['Position'].std() if len(driver_row) > 1 else 0,
                (driver_row['Position'] < 4).sum() / len(driver_row),
                (driver_row['Position'] > 10).sum() / len(driver_row),
            ]
            
            target = race_df[(race_df['Driver'] == driver) & 
                           (race_df['GrandPrix'] == gp_name)]['Position'].values
            
            if len(target) > 0:
                X.append(features)
                y.append(target[0])
    
    return np.array(X), np.array(y)

def prepare_full_features(race_df, qual_df, stats_df):
    print("Preparing full features...")
    
    all_race = pd.concat([race_df, qual_df], ignore_index=True)
    all_race = clean_race_results(all_race)
    
    X, y = create_sequences(all_race, qual_df, stats_df, n_races=5)
    
    print(f"Feature shape: {X.shape}, Target shape: {y.shape}")
    return X, y, all_race

def save_encoders(driver_enc, team_enc, scaler):
    with open(r"C:\Users\KARTIK MAHIDRAKAR\OneDrive\Desktop\python_ai\f1_project\encoders.pkl", 'wb') as f:
        pickle.dump({'driver': driver_enc, 'team': team_enc, 'scaler': scaler}, f)

def load_encoders():
    with open(r"C:\Users\KARTIK MAHIDRAKAR\OneDrive\Desktop\python_ai\f1_project\encoders.pkl", 'rb') as f:
        return pickle.load(f)

def preprocess_data():
    try:
        race_2024, race_2025, qual_2024, qual_2025, stats_2024, stats_2025 = load_cached_data()
        
        all_race = pd.concat([race_2024, race_2025], ignore_index=True)
        all_qual = pd.concat([qual_2024, qual_2025], ignore_index=True)
        all_stats = pd.concat([stats_2024, stats_2025], ignore_index=True)
        
        X, y, all_race = prepare_full_features(all_race, all_qual, all_stats)
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        np.save(r"C:\Users\KARTIK MAHIDRAKAR\OneDrive\Desktop\python_ai\f1_project\X_train.npy", X_scaled)
        np.save(r"C:\Users\KARTIK MAHIDRAKAR\OneDrive\Desktop\python_ai\f1_project\y_train.npy", y)
        
        print("Data preprocessing complete!")
        return X_scaled, y
    except Exception as e:
        print(f"Preprocessing error: {e}")
        return None, None

if __name__ == "__main__":
    preprocess_data()