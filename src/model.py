import pandas as pd
from xgboost import XGBClassifier
import joblib


def train_model(data_path: str, model_output: str):
    df = pd.read_csv(data_path)
    X = df.drop("winner", axis=1)
    y = df["winner"]

    model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
    model.fit(X, y)

    joblib.dump(model, model_output)
    print(f"✅ Model salvat în: {model_output}")


def predict_runda(model_path: str, input_data: pd.DataFrame):
    model = joblib.load(model_path)
    pred = model.predict(input_data)
    return pred


# 🔁 Permite rularea directă din terminal
if __name__ == "__main__":
    train_model("data/tracta_dataset_demo.csv", "models/tracta_model.pkl")