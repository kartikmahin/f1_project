import fastf1
import pandas as pd
import os
from datetime import datetime

cache_dir = r"C:\Users\KARTIK MAHIDRAKAR\OneDrive\Desktop\python_ai\f1_project\data_cache"
os.makedirs(cache_dir, exist_ok=True)
fastf1.Cache.enable_cache(cache_dir)

def load_race_data(year, grand_prix):
    try:
        session = fastf1.get_session(year, grand_prix, 'Race')
        session.load()
        return session
    except Exception as e:
        print(f"Error loading {grand_prix} {year}: {e}")
        return None

def get_all_race_results(year):
    races = fastf1.get_event_schedule(year)['EventName'].tolist()
    results = []
    
    for gp in races:
        if pd.isna(gp):
            continue
        session = load_race_data(year, gp)
        if session is None:
            continue
            
        try:
            race_results = session.results
            if race_results is not None and not race_results.empty:
                race_results['GrandPrix'] = gp
                race_results['Year'] = year
                results.append(race_results)
                print(f"Loaded: {gp} {year}")
        except Exception as e:
            print(f"Error getting results for {gp}: {e}")
    
    if results:
        return pd.concat(results, ignore_index=True)
    return pd.DataFrame()

def get_qualifying_results(year):
    races = fastf1.get_event_schedule(year)['EventName'].tolist()
    results = []
    
    for gp in races:
        if pd.isna(gp):
            continue
        try:
            session = fastf1.get_session(year, gp, 'Qualifying')
            session.load()
            qual_results = session.results
            if qual_results is not None and not qual_results.empty:
                qual_results['GrandPrix'] = gp
                qual_results['Year'] = year
                results.append(qual_results)
                print(f"Qualifying loaded: {gp}")
        except Exception as e:
            print(f"Error qualifying {gp}: {e}")
    
    if results:
        return pd.concat(results, ignore_index=True)
    return pd.DataFrame()

def get_driver_stats(year):
    races = fastf1.get_event_schedule(year)['EventName'].tolist()
    all_stats = []
    
    for gp in races:
        if pd.isna(gp):
            continue
        session = load_race_data(year, gp)
        if session is None:
            continue
            
        try:
            lap_data = session.laps
            if lap_data is not None and not lap_data.empty:
                fastest_by_driver = lap_data.groupby('Driver')['LapTime'].min().reset_index()
                fastest_by_driver['GrandPrix'] = gp
                fastest_by_driver['Year'] = year
                all_stats.append(fastest_by_driver)
        except Exception as e:
            print(f"Error stats for {gp}: {e}")
    
    if all_stats:
        return pd.concat(all_stats, ignore_index=True)
    return pd.DataFrame()

def collect_all_data():
    print("Collecting F1 data for 2024, 2025, and 2026...")
    
    years = [2024, 2025]
    for year in years:
        print(f"\n=== Collecting {year} ===")
        race_results = get_all_race_results(year)
        if not race_results.empty:
            race_results.to_csv(f"{cache_dir}/race_results_{year}.csv", index=False)
        
        qual_results = get_qualifying_results(year)
        if not qual_results.empty:
            qual_results.to_csv(f"{cache_dir}/qualifying_results_{year}.csv", index=False)
        
        driver_stats = get_driver_stats(year)
        if not driver_stats.empty:
            driver_stats.to_csv(f"{cache_dir}/driver_stats_{year}.csv", index=False)
    
    print("\nData collection complete!")
    return True

if __name__ == "__main__":
    collect_all_data()