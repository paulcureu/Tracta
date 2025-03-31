def gen_feedback(row: dict) -> str:
    feedback = []

    # Scoatem comparația cu "winner", că încă nu-l avem
    if row["entry_kill_team"] == 1:
        feedback.append("Echipa A a pierdut entry-ul. Atenție la deschideri!")

    if row["echipa_A_economy"] < 2500:
        feedback.append("Economie slabă pentru echipa A.")
    if row["echipa_B_economy"] < 2500:
        feedback.append("Economie slabă pentru echipa B.")

    if len(feedback) == 0:
        return "Rundă echilibrată. Nimic critic observat."

    return " ".join(feedback)