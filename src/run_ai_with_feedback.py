import pandas as pd
from model import predict_runda
from feedback import gen_feedback

# Exemplu de rundă nouă (input real sau simulat)
runda_input = {
    "echipa_A_rating": 1.08,
    "echipa_B_rating": 0.97,
    "echipa_A_economy": 6200,
    "echipa_B_economy": 3500,
    "entry_kill_team": 1,
    "mapa": 2
}

# Pregătim datele pentru model (DataFrame cu o singură linie)
df_input = pd.DataFrame([runda_input])

# Predicție AI (folosim modelul salvat anterior)
pred = predict_runda("models/tracta_model.pkl", df_input)
pred_label = "echipa A" if pred[0] == 0 else "echipa B"

# Feedback tactic generat pe acea rundă
feedback = gen_feedback(runda_input)

# Afișăm rezultatele
print("🔮 Predicție AI: Va câștiga:", pred_label)
print("🧠 Feedback tactic:", feedback)
