from flask import render_template, request, redirect, flash, session
from hospital_management_system.models import User, Patient
from hospital_management_system import app, db
from datetime import datetime

@app.route('/')
def home():
    db.create_all()
    db.session.commit()
    if not session.get("username"):
        return redirect("/login")
    return render_template('home.html')


@app.route('/login', methods=["GET","POST"])
def login():
    if session.get("username"):
        return redirect("/")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        admin = User.query.filter_by(username='admin').first()
        if admin and password == admin.password:
            session["user_id"] = admin.user_id
            session["username"] = username
            return redirect("/")
        else:
            flash("Sorry, something went wrong.")

    return render_template('login.html', Login=True)

@app.route("/logout")
def logout():
    session["user_id"] = False
    session["username"] = False
    return redirect("/login")

@app.route("/patient")
def patient():
    if not session.get("username"):
        return redirect("/login")
    return render_template("patient_base.html", patient="active")

@app.route("/patient_register")
def patient_register():
    data = {}
    if not session.get("username"):
        return redirect("/login")
    data["today_date"] = datetime.now().date()
    if request.method == "POST":
        p_id = request.form.get("PatientSSN")
        p_name = request.form.get("PatientName")
        age = request.form.get("PatientAge")
        date = request.form.get("DateOfAdmin")
        bed = request.form.get("Bed")
        address = request.form.get("Address")
        state = request.form.get("State")
        city = request.form.get("City")
        
        patient = Patient(ssid=p_id, name=p_name, age=age, date_of_admission=date, type_of_bed=bed, address=address, state=state, city=city, status="Active")
        db.session.add(patient)
        db.session.commit()

        flash("Successfully Patient Added!!")

    return render_template("patient_register.html", patient="active", data=data)






    