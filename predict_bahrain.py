import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

DATA_DIR = r"C:\Users\KARTIK MAHIDRAKAR\OneDrive\Desktop\python_ai\f1_project\data_cache"
OUTPUT_PATH = r"C:\Users\KARTIK MAHIDRAKAR\OneDrive\Desktop\python_ai\f1_project\bahrain_predictions_2026.csv"

def get_driver_score(driver_data):
    if len(driver_data) == 0:
        return 100
    
    recent = driver_data.tail(10)
    avg_pos = recent['Position'].mean()
    avg_std = recent['Position'].std() if len(recent) > 1 else 0
    points = recent['Points'].sum()
    podiums = (recent['Position'] <= 3).sum()
    wins = (recent['Position'] == 1).sum() * 2
    
    score = avg_pos - (podiums * 0.5) - (wins * 0.3) + (avg_std * 0.1)
    
    return max(1, score)

def predict_bahrain():
    df = pd.read_csv(f"{DATA_DIR}/all_race_results.csv")
    
    drivers_2026 = ['VER', 'NOR', 'LEC', 'HAM', 'RUS', 'ALO', 'PIA', 'SAI', 'GAS', 'ALB',
                  'OCO', 'MAG', 'ZHO', 'BOT', 'STR', 'PER', 'TSU', 'KVY', 'DEV', 'LAW']
    teams = {
        'VER': 'Red Bull Racing', 'PER': 'Red Bull Racing',
        'NOR': 'McLaren', 'PIA': 'McLaren', 'SAI': 'McLaren',
        'LEC': 'Ferrari', 'HAM': 'Mercedes', 'RUS': 'Mercedes',
        'ALO': 'Aston Martin', 'GAS': 'Alpine', 'OCO': 'Alpine',
        'ALB': 'Williams', 'MAG': 'Haas', 'ZHO': 'Alfa Romeo',
        'BOT': 'Haas', 'STR': 'Aston Martin', 'TSU': 'AlphaTauri',
        'KVY': 'AlphaTauri', 'DEV': 'Racing Bulls', 'LAW': 'Racing Bulls'
    }
    
    results = []
    
    for driver in drivers_2026:
        driver_data = df[df['Driver'] == driver]
        score = get_driver_score(driver_data)
        
        results.append({
            'Driver': driver,
            'Team': teams.get(driver, 'Unknown'),
            'Score': score
        })
    
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('Score')
    results_df = results_df.reset_index(drop=True)
    results_df.index = results_df.index + 1
    results_df.index.name = 'PredictedFinish'
    
    print("\n" + "="*60)
    print("BAHRAIN GRAND PRIX 2026 - PREDICTED STANDINGS")
    print("="*60)
    for idx, row in results_df.iterrows():
        print(f"{idx:2d}. {row['Driver']:4s} ({row['Team']:<18s}) -> Score: {row['Score']:.1f}")
    print("="*60)
    
    results_df.to_csv(OUTPUT_PATH)
    print(f"\nPredictions saved to {OUTPUT_PATH}")
    
    return results_df

if __name__ == "__main__":
    predict_bahrain()