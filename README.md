# Tracta – AI Tactical Coach for CS2

**Tracta** este o platformă de analiză tactică și predicție AI pentru meciurile de CS2. Proiectul oferă feedback inteligent pentru jucători, echipe, antrenori, streameri și analiști.

## 🔍 Funcționalități

- Predicție rundă, hartă și meci bazată pe date live și istorice
- Feedback tactic automat pe baza acțiunilor din joc
- Rapoarte detaliate post-meci pentru echipe și jucători
- HUD și overlay-uri live pentru streameri
- Generator de cote și probabilități pentru analiști de pariuri

## 📦 Structură Proiect

```bash
Tracta/
├── data/           # Fișiere .csv, .json, .dem, date brute
├── models/         # Modele AI antrenate și salvate (.pkl, .joblib)
├── notebooks/      # Jupyter Notebooks pentru explorare și testare
├── src/            # Cod sursă Python (model, feedback, preprocesare)
│   ├── model.py
│   ├── feedback.py
│   └── ...
├── app/            # Interfață Streamlit / Flask pentru demo MVP
├── tests/          # Teste unitare
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Tehnologii folosite

- Python 3.11+
- pandas, scikit-learn, xgboost
- streamlit / flask (pentru UI)
- joblib / pickle (pentru salvare model)

## 🚀 Cum rulezi proiectul

```bash
# activează mediul virtual
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

# instalează dependințele
pip install -r requirements.txt

# rulează aplicația (exemplu Streamlit)
streamlit run app/main.py
```

## 📬 Contact & Contribuție

Proiect aflat în stadiu MVP. Feedback, contribuții și idei sunt binevenite.

---

# 🧠 src/model.py (versiune de start)
