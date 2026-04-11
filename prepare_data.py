import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder, StandardScaler

DATA_DIR = r"C:\Users\KARTIK MAHIDRAKAR\OneDrive\Desktop\python_ai\f1_project\data_cache"

def create_sample_data():
    np.random.seed(42)
    
    drivers = ['VER', 'NOR', 'LEC', 'HAM', 'RUS', 'ALO', 'PIA', 'SAI', 'GAS', 'ALB',
              'OCO', 'MAG', 'ZHO', 'BOT', 'STR', 'PER', 'TSU', 'KVY', 'DEV', 'LAW']
    teams = ['Red Bull Racing', 'McLaren', 'Ferrari', 'Mercedes', 'Aston Martin', 
            'Alpine', 'Williams', 'Haas', 'Alfa Romeo', 'AlphaTauri']
    
    data = []
    years = [2024, 2025]
    gps = ['Bahrain GP', 'Saudi GP', 'Australian GP', 'Japanese GP', 'Chinese GP',
           'Miami GP', 'Monaco GP', 'Canadian GP', 'Spanish GP', 'British GP',
           'Austrian GP', 'Belgian GP', 'Dutch GP', 'Italian GP', 'Singapore GP',
           'Azerbaijan GP', 'United States GP', 'Mexico GP', 'Brazil GP', 'Abu Dhabi GP']
    
    for year in years:
        for gp_idx, gp in enumerate(gps):
            base_perf = {d: np.random.normal(10, 5) for d in drivers}
            
            for team in ['Red Bull Racing']:
                for d in ['VER', 'PER']: base_perf[d] -= 4
            for team in ['McLaren']:
                for d in ['NOR', 'PIA', 'SAI']: base_perf[d] -= 3
            for team in ['Ferrari']:
                for d in ['LEC']: base_perf[d] -= 3
            for team in ['Mercedes']:
                for d in ['HAM', 'RUS']: base_perf[d] -= 2
            
            positions = sorted(base_perf.items(), key=lambda x: x[1])
            
            for pos, (driver, score) in enumerate(positions, 1):
                team = drivers.index(driver) % len(teams)
                grid = max(1, pos + np.random.randint(-3, 4))
                
                data.append({
                    'Driver': driver,
                    'Team': teams[team],
                    'Position': pos,
                    'GridPosition': grid,
                    'Points': max(0, 25 - pos * 2) if pos <= 10 else 0,
                    'GrandPrix': gp,
                    'Year': year
                })
    
    df = pd.DataFrame(data)
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(f"{DATA_DIR}/all_race_results.csv", index=False)
    print(f"Created sample data: {len(df)} records")
    return df

def preprocess_data():
    df = pd.read_csv(f"{DATA_DIR}/all_race_results.csv")
    
    driver_enc = LabelEncoder()
    team_enc = LabelEncoder()
    
    df['DriverEnc'] = driver_enc.fit_transform(df['Driver'])
    df['TeamEnc'] = team_enc.fit_transform(df['Team'])
    
    df = df.sort_values(['Year', 'GrandPrix', 'Position'])
    
    features = []
    targets = []
    
    for driver in df['Driver'].unique():
        driver_df = df[df['Driver'] == driver].sort_values(['Year', 'GrandPrix'])
        
        for i in range(5, len(driver_df)):
            past = driver_df.head(i)
            last_5 = past.tail(5)
            
            feat = [
                driver_enc.transform([driver])[0],
                team_enc.transform([past['Team'].iloc[-1]])[0],
                last_5['Position'].mean(),
                last_5['Position'].std() if len(last_5) > 1 else 0,
                last_5['Position'].iloc[-1],
                last_5['Position'].iloc[-2] if len(last_5) > 1 else 10,
                last_5['Points'].sum(),
                (last_5['Position'] <= 3).sum(),
            ]
            features.append(feat)
            
            target = driver_df.iloc[i]['Position']
            targets.append(target)
    
    X = np.array(features, dtype=np.float32)
    y = np.array(targets, dtype=np.float32)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    np.save(r"C:\Users\KARTIK MAHIDRAKAR\OneDrive\Desktop\python_ai\f1_project\X_train.npy", X_scaled)
    np.save(r"C:\Users\KARTIK MAHIDRAKAR\OneDrive\Desktop\python_ai\f1_project\y_train.npy", y)
    
    print(f"Preprocessed: X={X_scaled.shape}, y={y.shape}")
    return X_scaled, y

if __name__ == "__main__":
    create_sample_data()
    preprocess_data()