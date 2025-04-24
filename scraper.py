import pandas as pd
from datetime import date

def fetch_daily_race_data():
    today = date.today().strftime("%Y-%m-%d")
    races = []
    for race_num in range(1, 13):
        for lane in range(1, 7):
            races.append({
                "レースID": f"{today}_{race_num}R",
                "枠番": lane,
                "勝率": round(4.5 + lane * 0.2, 1),
                "ST平均": round(0.15 + lane * 0.01, 2),
                "展示タイム": round(6.70 - lane * 0.02, 2),
                "風速": round(2.0 + (lane % 3) * 0.3, 1),
                "着順": lane,
                "オッズ": round(2.0 + (7 - lane) * 1.5, 1)
            })
    return pd.DataFrame(races)
