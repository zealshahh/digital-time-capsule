""" Flask app for creating time capsules. """

from flask import Flask, render_template, request, session, redirect, url_for
import os
from datetime import datetime, timedelta
import random


app = Flask(__name__, template_folder="templates")
app.secret_key = "supersecretkey"  # Needed for session storage

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Simulated database (replace with real database later)
capsule_data = {}


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/createCapsule")
def createCapsule():
    return render_template("createCapsule.html")


@app.route("/step1", methods=["GET", "POST"])
def step1():
    if request.method == "POST":
        capsule_name = request.form.get("capsule_name")
        if not capsule_name.strip():  # Ensure it's not empty or just spaces
            return "Capsule name cannot be empty!", 400
        session["capsule_name"] = capsule_name  # Store in session
        return redirect(url_for("step2"))  # Move to the next step
    return render_template("step1.html")

@app.route("/step2", methods=["GET", "POST"])
def step2():
    if request.method == "POST":
        files = request.files.getlist("files")
        uploaded_files = []
        for file in files:
            if file.filename:
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file.save(filepath)
                uploaded_files.append(filepath)
        session["uploaded_files"] = uploaded_files
        return redirect(url_for("step3"))
    return render_template("step2.html")

@app.route("/step3", methods=["GET", "POST"])
def step3():
    if request.method == "POST":
        date_choice = request.form["date_choice"]
        if date_choice == "random":
            open_date = datetime.now() + timedelta(days=random.randint(30, 365))  # Random date within 1 year
        else:
            open_date = datetime.strptime(request.form["specific_date"], "%Y-%m-%d")
        session["open_date"] = open_date.strftime("%Y-%m-%d")
        return redirect(url_for("step4"))
    return render_template("step3.html")

@app.route("/step4", methods=["GET", "POST"])
def step4():
    if request.method == "POST":
        email = request.form["email"]
        capsule_id = len(capsule_data) + 1  # Simulate unique ID
        capsule_data[capsule_id] = {
            "name": session.get("capsule_name"),
            "files": session.get("uploaded_files"),
            "open_date": session.get("open_date"),
            "email": email,
        }
        return render_template("confirmation.html", capsule_id=capsule_id)
    return render_template("step4.html")

if __name__ == "__main__":
    app.run(debug=True)
