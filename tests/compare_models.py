import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical

# Încarcă datele
df = pd.read_csv("data/tracta_dataset_demo.csv")
X = df.drop("winner", axis=1)
y = df["winner"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ----------------------
# MODEL 1 – XGBoost
# ----------------------
xgb_model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
xgb_model.fit(X_train, y_train)
xgb_preds = xgb_model.predict(X_test)
xgb_acc = accuracy_score(y_test, xgb_preds)

# ----------------------
# MODEL 2 – Neural Network (Keras)
# ----------------------
# Normalizare
X_train_nn = X_train / X_train.max()
X_test_nn = X_test / X_train.max()

# Convertim etichetele
y_train_cat = to_categorical(y_train, num_classes=2)
y_test_cat = to_categorical(y_test, num_classes=2)

# Rețea neuronală simplă
nn_model = Sequential([
    Dense(16, input_shape=(X_train.shape[1],), activation='relu'),
    Dense(8, activation='relu'),
    Dense(2, activation='softmax')
])
nn_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
nn_model.fit(X_train_nn, y_train_cat, epochs=50, verbose=0)

# Evaluare
_, nn_acc = nn_model.evaluate(X_test_nn, y_test_cat, verbose=0)

# 🔍 COMPARAȚIE
print(f"🎯 XGBoost Accuracy:        {xgb_acc:.2f}")
print(f"🧠 Neural Network Accuracy: {nn_acc:.2f}")
