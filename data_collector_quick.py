import fastf1
import pandas as pd
import os

cache_dir = r"C:\Users\KARTIK MAHIDRAKAR\OneDrive\Desktop\python_ai\f1_project\data_cache"
os.makedirs(cache_dir, exist_ok=True)
fastf1.Cache.enable_cache(cache_dir)

def get_race_results(year, gp_name):
    try:
        session = fastf1.get_session(year, gp_name, 'Race')
        session.load()
        results = session.results
        if results is not None:
            results['GrandPrix'] = gp_name
            results['Year'] = year
            return results
    except Exception as e:
        print(f"Error {gp_name}: {e}")
    return None

def collect_quick_data():
    print("Collecting quick sample data...")
    
    races_2024 = ['Bahrain Grand Prix', 'Saudi Arabian Grand Prix', 'Australian Grand Prix', 'Japanese Grand Prix', 'Chinese Grand Prix']
    races_2025 = ['Bahrain Grand Prix', 'Saudi Arabian Grand Prix', 'Australian Grand Prix', 'Japanese Grand Prix', 'Chinese Grand Prix']
    
    all_results = []
    
    for year, race_list in [(2024, races_2024), (2025, races_2025)]:
        for gp in race_list:
            result = get_race_results(year, gp)
            if result is not None:
                all_results.append(result)
                print(f"Loaded: {gp} {year}")
    
    if all_results:
        df = pd.concat(all_results, ignore_index=True)
        df.to_csv(f"{cache_dir}/all_race_results.csv", index=False)
        print(f"Saved {len(df)} records")
        return df
    return pd.DataFrame()

if __name__ == "__main__":
    collect_quick_data()