import pandas as pd
import itertools
from lightgbm import LGBMClassifier

def load_model():
    df = pd.read_csv("model_data.csv")
    df["1着か"] = (df["着順"] == 1).astype(int)
    features = ["枠番", "勝率", "ST平均", "展示タイム", "風速"]
    X = df[features]
    y = df["1着か"]
    model = LGBMClassifier()
    model.fit(X, y)
    return model

def predict_race(df, model):
    features = ["枠番", "勝率", "ST平均", "展示タイム", "風速"]
    preds = model.predict_proba(df[features])[:, 1]
    df["1着確率"] = (preds * 100).round(1)
    df["荒れ度"] = abs(preds - 0.5).round(2)
    df["期待値"] = (df["オッズ"] * preds).round(2)
    top3 = df.sort_values("1着確率", ascending=False).head(3)["枠番"].tolist()
    sanrentan = list(itertools.permutations(top3, 3))
    df["3連単候補"] = ', '.join('-'.join(map(str, s)) for s in sanrentan)
    return df

def predict_all_races(full_df):
    model = load_model()
    output = []
    for race_id, race_df in full_df.groupby("レースID"):
        if len(race_df) != 6:
            continue
        pred_df = predict_race(race_df.copy(), model)
        output.append({
            "race_id": race_id,
            "data": pred_df.to_dict(orient="records")
        })
    return output
