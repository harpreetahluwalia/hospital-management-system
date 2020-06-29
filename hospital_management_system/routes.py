from flask import render_template, request, redirect, flash, session, jsonify
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


@app.route("/patient_register", methods=["GET","POST"])
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
        date = datetime.strptime(date,'%Y-%m-%d')
        bed = request.form.get("Bed")
        address = request.form.get("Address")
        state = request.form.get("State")
        city = request.form.get("City")
        if len(Patient.query.all()) > 0:
            patient = Patient(ssid=p_id, name=p_name, age=age, date_of_admission=date, type_of_bed=bed, address=address, state=state, city=city, status="Active")
            db.session.add(patient)
            db.session.commit()
        else:
            patient = Patient(id=1000000000,ssid=p_id, name=p_name, age=age, date_of_admission=date, type_of_bed=bed, address=address, state=state, city=city, status="Active")
            db.session.add(patient)
            db.session.commit()

        flash("Successfully Patient Added!!")

    return render_template("patient_register.html", patient="active", data=data)

@app.route("/patient_list")
def patient_list():
    if not session.get("username"):
        return redirect("/login")

    patients = Patient.query.all()
    
    return render_template("patient_list.html", patient="active", patients=patients)

@app.route("/patient_update", methods=["GET","POST"])
def patient_update():
    if not session.get("username"):
        return redirect("/login")
    if request.method == "POST":
        p_id = request.form.get("PatientId")
        p_name = request.form.get("PatientName")
        age = request.form.get("PatientAge")
        date = request.form.get("DateOfAdmin")
        date = datetime.strptime(date,'%Y-%m-%d')
        bed = request.form.get("Bed")
        address = request.form.get("Address")
        state = request.form.get("State")
        city = request.form.get("City")
        
        data = dict(
            name = p_name, 
            age = age, 
            date_of_admission = date, 
            type_of_bed = bed, 
            address = address, 
            state = state, 
            city = city, 
            status = "Active"
        )
        patient = Patient.query.filter_by(id=p_id).update(data)
        
        db.session.commit()

        flash("Successfully Patient Updated!!")

    return render_template("patient_update.html", patient="active")

@app.route("/get_patient", methods=["GET","POST"])
def get_patient():
    data={}
    if "pid" in request.args:
        pid = request.args.get("pid")
        patient = Patient.query.filter_by(id=pid).first()
        if patient:
            data["status"] = True
            #data["id"] = patient.id
            data["name"] = patient.name
            data["age"] = patient.age
            data["date"] = str(patient.date_of_admission)
            data["address"] = patient.address
            data["city"] = patient.city
            data["state"] = patient.state
            data["bed"] = patient.type_of_bed
        else:
            data["status"] = False
    return jsonify(data)