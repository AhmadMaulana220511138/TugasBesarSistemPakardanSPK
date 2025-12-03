from flask import Flask, render_template, request
from flask import send_from_directory


app = Flask(__name__)

def fuzzy_recommendation(risk):
    r = risk / 10
    risky_asset = r * 100
    safe_asset = (1 - r) * 100
    return risky_asset, safe_asset


def investment_recommendation(risk, goal, duration):
    rekom = []

    # Risiko pengguna
    if risk <= 3:
        risk_level = "konservatif"
    elif risk <= 7:
        risk_level = "moderat"
    else:
        risk_level = "agresif"

    # Rule berdasarkan risiko
    if risk_level == "konservatif":
        rekom += ["Deposito Berjangka", "Obligasi Pemerintah (ORI/SBR)"]
        if duration > 5:
            rekom.append("Emas Batangan (Aman Jangka Panjang)")

    elif risk_level == "moderat":
        rekom += ["Reksadana Campuran", "Emas"]
        if duration >= 5:
            rekom.append("Saham Blue Chip (Stabil & Terukur)")

    elif risk_level == "agresif":
        rekom += ["Saham Blue Chip", "Reksadana Saham"]
        if duration >= 5:
            rekom.append("Saham Sektor Pertumbuhan (Teknologi, Energi)")

    # Rule tujuan finansial
    if goal == "pendek":
        rekom.append("Reksadana Pasar Uang (Likuid & Rendah Risiko)")
    elif goal == "menengah":
        rekom.append("Obligasi Korporasi / Sukuk Ritel")
    elif goal == "panjang":
        rekom.append("Portofolio Diversifikasi Jangka Panjang")

    return rekom


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        risk_value = float(request.form["risk"])
        goal = request.form["goal"]
        duration = int(request.form["duration"])

        risky, safe = fuzzy_recommendation(risk_value)
        rekom_list = investment_recommendation(risk_value, goal, duration)

        result = {
            "risk": risk_value,
            "goal": goal,
            "duration": duration,
            "risky": round(risky, 1),
            "safe": round(safe, 1),
            "recommendations": rekom_list
        }

    return render_template("index.html", result=result)


# ✅ Route untuk halaman investasi
@app.route("/investasi", methods=["GET", "POST"])
def investasi():
    result = None
    if request.method == "POST":
        risk_value = float(request.form["risk"])
        goal = request.form["goal"]
        duration = int(request.form["duration"])

        risky, safe = fuzzy_recommendation(risk_value)
        rekom_list = investment_recommendation(risk_value, goal, duration)

        result = {
            "risk": risk_value,
            "goal": goal,
            "duration": duration,
            "risky": round(risky, 1),
            "safe": round(safe, 1),
            "recommendations": rekom_list
        }

    return render_template("investasi.html", result=result)


@app.route('/img/<path:filename>')
def serve_image(filename):
    return send_from_directory('img', filename)




if __name__ == "__main__":
    app.run(debug=True)
