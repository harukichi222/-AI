from flask import Flask, render_template
import pandas as pd
from predictor import predict_all_races
from scraper import fetch_daily_race_data

app = Flask(__name__)

@app.route("/")
def index():
    try:
        raw_df = fetch_daily_race_data()
        race_results = predict_all_races(raw_df)
        return render_template("index.html", races=race_results)
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
