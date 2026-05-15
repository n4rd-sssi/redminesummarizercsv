from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["file"]

    df = pd.read_csv(file, encoding="cp1252")

    df["Assignee"] = df["Assignee"].fillna("Unassigned")

    grouped = {}

    for _, row in df.iterrows():

        assignee = row["Assignee"]

        ticket = {
            "id": row["#"],
            "subject": row["Subject"],
            "status": row["Status"],
            "tracker": row["Tracker"],
            "percent": row["% Done"]
        }

        grouped.setdefault(assignee, []).append(ticket)

    return jsonify(grouped)

if __name__ == "__main__":
    app.run(debug=True)