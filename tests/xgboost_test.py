import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier

# Încarcă datasetul
df = pd.read_csv("data/tracta_dataset_demo.csv")
X = df.drop("winner", axis=1)
y = df["winner"]

# Împărțim în train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model XGBoost
model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
model.fit(X_train, y_train)

# Predicție + scor
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print(f"Acuratețea modelului XGBoost pe test set: {acc:.2f}")
