from flask import render_template, request, redirect, flash, session, jsonify, url_for
from hospital_management_system.models import User, Patient, Medicines, MedicinesIssued, MedicinesIssued, Diagnostic_test, DiagnosticIssued
from hospital_management_system import app, db
from datetime import datetime


@app.route('/', methods=["GET","POST"])
def login():
    # if session.get("username"):
    #     if session.get("username") == "admin":
    #         return redirect("/patient_register")

    #     elif session.get("username") == "pharma":
    #         return redirect("/issue_medicines")
        
    #     elif session.get("username") == "diagnostic":
    #         return redirect("/diag_patient_details")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        admin = User.query.filter_by(username=username).first()
        if admin and password == admin.password:
            session["user_id"] = admin.user_id
            session["username"] = username
            if username == "admin":
                return redirect("/patient_register")
            elif username == "pharma":
                return redirect("/issue_medicines")
            elif username == "diagnostic":
                return redirect("/diag_patient_details")
        else:
            flash("Sorry, something went wrong.")

    return render_template('login.html', Login=True)

@app.route("/logout")
def logout():
    session["user_id"] = False
    session["username"] = False
    return redirect("/")


@app.route("/patient_register", methods=["GET","POST"])
def patient_register():
    data = {}
    if not session.get("username"):
        return redirect("/")
    if session.get("username") != "admin":
        return redirect("/")
    data["today_date"] = datetime.now().date()
    if request.method == "POST":
        p_id = request.form.get("PatientSSN")
        p_name = request.form.get("PatientName")
        age = request.form.get("PatientAge")
        date = data["today_date"]
        bed = request.form.get("Bed")
        address = request.form.get("Address")
        state = request.form.get("State")
        city = request.form.get("City")
        if len(Patient.query.all()) > 0:
            patient = Patient(ssid=p_id, name=p_name, age=age, date_of_admission=date, type_of_bed=bed, address=address, state=state, city=city, status="Active")
            db.session.add(patient)
            db.session.commit()
        else:
            patient = Patient(id=100000000,ssid=p_id, name=p_name, age=age, date_of_admission=date, type_of_bed=bed, address=address, state=state, city=city, status="Active")
            db.session.add(patient)
            db.session.commit()

        flash("Successfully Patient Added!!")

    return render_template("patient_register.html", patient="active", data=data, username=session.get("username"))

@app.route("/patient_list")
def patient_list():
    if not session.get("username"):
        return redirect("/")
    if session.get("username") != "admin":
        return redirect("/")
    patients = Patient.query.all()
    
    return render_template("patient_list.html", patient="active", patients=patients, username=session.get("username"))

@app.route("/patient_update", methods=["GET","POST"])
def patient_update():
    if not session.get("username"):
        return redirect("/")
    if session.get("username") != "admin":
        return redirect("/")
    if request.method == "POST":
        p_id = request.form.get("PatientId")
        p_name = request.form.get("PatientName")
        age = request.form.get("PatientAge")
        # date = request.form.get("DateOfAdmin")
        # date = datetime.strptime(date,'%Y-%m-%d')
        bed = request.form.get("Bed")
        address = request.form.get("Address")
        state = request.form.get("State")
        city = request.form.get("City")
        
        data = dict(
            name = p_name, 
            age = age, 
            # date_of_admission = date, 
            type_of_bed = bed, 
            address = address, 
            state = state, 
            city = city, 
            # status = "Active"
        )
        patient = Patient.query.filter_by(id=p_id).update(data)
        db.session.commit()
        flash("Successfully Patient Updated!!")
    return render_template("patient_update.html", username=session.get("username"))

@app.route("/get_patient", methods=["GET","POST"])
def get_patient():
    data={}
    if not session.get("username"):
        return redirect("/")
    
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


@app.route("/check_patient", methods=["GET","POST"])
def check_patient():
    data={}
    if not session.get("username"):
        return redirect("/")
    if "pssn" in request.args:
        pssn = request.args.get("pssn")
        patient = Patient.query.filter_by(ssid=pssn).first()
        if patient:
            data["status"] = False
        else:
            data["status"] = True
    return jsonify(data)

@app.route("/patient_delete", methods=["GET","POST"])
def patient_delete():
    if not session.get("username"):
        return redirect("/")
    if session.get("username") != "admin":
        return redirect("/")
    if request.method == "POST":
        p_id = request.form.get("PatientId")
        patient = Patient.query.filter_by(id=p_id).first()
        db.session.delete(patient)
        db.session.commit()
        flash("Successfully Patient Deleted!!")
    return render_template("patient_delete.html", username=session.get("username"))

@app.route("/patient_view", methods=["GET","POST"])
def patient_view():
    if not session.get("username"):
        return redirect("/")
    if session.get("username") != "admin":
        return redirect("/")
    return render_template("patient_view.html", username=session.get("username"))


@app.route("/issue_medicines", methods=["GET","POST"])
def issue_medicines():
    data = {}
    if not session.get("username"):
        return redirect("/")
    if session.get("username") != "pharma":
        return redirect("/")
    meds = Medicines.query.all()
    med_is = ""
    if "pid" in request.args.keys():
        p_id = request.args.get("pid")
        patient = Patient.query.filter_by(id=p_id).first()
        if patient:
            med_is = MedicinesIssued.query.filter_by(p_id=p_id)
            if request.method == "GET":
                flash("Patient Found Successfully!")
            data["found"] = True
        else:
            patient = ["id", "name", "age", "address", "doj", "type of room"]
            flash("Patient With this Id not found!!")
    else:
        patient = ["id", "name", "age", "address", "doj", "type of room"]
    
    if request.method=='POST':
        if "add" in request.form.keys():
            name = request.form.get("name")
            quantity = request.form.get("quantity")
            rate = request.form.get("rate")
            med = Medicines(name=name,quantity_available=quantity,rate=rate)
            db.session.add(med)
            db.session.commit()
            flash("Successfully Medicine Added!")
            return redirect("/issue_medicines")
        
        if "issue" in request.form.keys():
            p_id = request.form.get("p_id")
            med_id = request.form.get("med")
            quantity = request.form.get("quantity")
            med = Medicines.query.filter_by(id=med_id).first()
            result = int(med.quantity_available) - int(quantity)
            med = Medicines.query.filter_by(id=med_id).update(dict(quantity_available=result))
            db.session.commit()
            med_issue = MedicinesIssued(p_id=p_id,med_id=med_id, quantity=quantity)
            db.session.add(med_issue)
            db.session.commit()
            flash("Medicine Added in Issue List Sucessfully!!")
        
        if "update" in request.form.keys():
            flash("Medicines issued successfully!!")

    return render_template("issueMedicines.html", meds=meds, patient=patient, med_is=med_is, data=data, username=session.get("username"))

@app.route("/check_med", methods=["GET","POST"])
def check_med():
    data={}
    if not session.get("username"):
        return redirect("/")

    if "med_id" in request.args:
        med_id = request.args.get("med_id")
        med = Medicines.query.filter_by(id=med_id).first()
        if int(med.quantity_available) > 0:
            data["status"] = True
        else:
            data["status"] = False
    return jsonify(data)

@app.route("/check_quantity", methods=["GET","POST"])
def check_quantity():
    data={}
    if not session.get("username"):
        return redirect("/")

    if "med_id" in request.args:
        med_id = request.args.get("med_id")
        quantity = request.args.get("quantity")
        med = Medicines.query.filter_by(id=med_id).first()
        result = int(med.quantity_available) - int(quantity)
        if result >= 0:
            data["status"] = True
        else:
            data["status"] = False
            data["q"] = med.quantity_available
    return jsonify(data)


#Diagnostics Screen
#Get Patient Details
@app.route("/diag_patient_details", methods=["GET","POST"])
def diag_patient_details():
    if not session.get("username"):
        return redirect("/")
    if session.get("username") != "diagnostic":
        return redirect("/")
    if request.method == "POST":
        pid = request.form.get("PatientId")
        pat = Patient.query.filter_by(id=pid).first()
        if pat:
            return redirect(url_for('diagnostics_add', pid=pid))
        else:
            return render_template("diag_patient_details.html")
    return render_template("diag_patient_details.html", username=session.get("username"))

#Add new test
@app.route("/diag_test_add", methods=["GET","POST"])
def diag_test_add():
    if not session.get("username"):
        return redirect("/")
    if session.get("username") != "diagnostic":
        return redirect("/")
    if request.method == "POST":
        name = request.form.get("TestName")
        cost = request.form.get("TestCost")
        dia = Diagnostic_test(test_name=name, test_cost=cost)
        db.session.add(dia)
        db.session.commit()
        flash("Successfully New Diagnostic Test Added!")
        #return redirect("/diag_patient_details")
    return render_template("diag_test_add.html", username=session.get("username"))


#Add Diagnostics
@app.route("/diagnostics_add/<pid>", methods=["GET","POST"])
def diagnostics_add(pid):
    if not session.get("username"):
        return redirect("/")
    if session.get("username") != "diagnostic":
        return redirect("/")
    #get diagnostics conducted
    obj = Diagnostic_test.query.all()
    res = DiagnosticIssued.query.filter_by(p_id=pid).all()
    lis=[]
    for p in res:
        lis.append(p.test_id)
    d={}
    result = Diagnostic_test.query.all()
    for i in result:
        d[i.id] = (i.test_name, i.test_cost)
    new=[]
    for j in lis:
        new.append([d[j][0], d[j][1]])

    #get medicines issued
    medres = MedicinesIssued.query.filter_by(p_id=pid).all()
    medid = []
    for m in medres:
        medid.append(m.id)
    med=[]
    for a in medid:
        med.append(Medicines.query.get(1).name)


    if request.method == "POST":
        test_name = request.form.get("test")
        test = Diagnostic_test.query.filter_by(test_name=test_name).first()
        p = DiagnosticIssued.query.filter_by(test_id=test.id).first()
        
        diag = DiagnosticIssued(p_id=pid, test_id=test.id)
        db.session.add(diag)
        db.session.commit()
        flash("Diagnostic Added Sucessfully!!")
        return redirect(url_for('diagnostics_add', pid=pid))
    return render_template("diagnostics_add.html", obj = obj, pid=pid, new = new, med=med, username=session.get("username"))

#get_diagnostic test charge
@app.route("/get_diagnostic", methods=["GET","POST"])
def get_diagnostic():
    data={}
    if not session.get("username"):
        return redirect("/")

    if "dname" in request.args:
        dname = request.args.get("dname")
        test = Diagnostic_test.query.filter_by(test_name=dname).first()
        if test:
            data["cost"] = test.test_cost
    return jsonify(data)

@app.route("/final_billing", methods=["GET","POST"])
def final_billing():
    data = {}
    if not session.get("username"):
        return redirect("/")
    if session.get("username") != "admin":
        return redirect("/")
    meds = Medicines.query.all()
    tests = Diagnostic_test.query.all()
    med_is = ""
    test_is = ""
    if "pid" in request.args.keys():
        p_id = request.args.get("pid")
        patient = Patient.query.filter_by(id=p_id).first()
        if patient:
            data["today_date"] = datetime.now().date()
            data["days"] = str(data["today_date"] - patient.date_of_admission)[0]
            room_bill = ""
            if patient.type_of_bed == "General Ward":
                data["room_bill"] = int(data["days"]) * 2000
                room_bill = int(data["days"]) * 2000
            elif patient.type_of_bed == "Semi Sharing":
                data["room_bill"] = int(data["days"]) * 4000
                room_bill = int(data["days"]) * 4000
            else:
                data["room_bill"] = int(data["days"]) * 8000
                room_bill = int(data["days"]) * 8000
            med_is = MedicinesIssued.query.filter_by(p_id=p_id)
            p_bill = []
            for i in med_is:
                for j in meds:
                    if i.med_id == j.id:
                        p_bill.append(j.rate*i.quantity)
            data["p_bill"] = sum(p_bill)
            test_is = DiagnosticIssued.query.filter_by(p_id=p_id)
            test_bill = []
            for i in test_is:
                for j in tests:
                    if i.test_id == j.id:
                       test_bill.append(j.test_cost)
            data["test_bill"] = sum(test_bill)         
            data["total_bill"] = data["test_bill"] + data["p_bill"] + room_bill         
            if request.method == "GET":
                flash("Patient Found Successfully!")
        else:
            patient = ["id", "name", "age", "address", "doj", "type of room"]
            flash("Patient With this Id not found!!")
    else:
        patient = ["id", "name", "age", "address", "doj", "type of room"]

    if request.method == "POST":
        p_id = request.args.get("pid")
        patient = Patient.query.filter_by(id=p_id).update(dict(status="Discharged"))
        db.session.commit()
        patient = Patient.query.filter_by(id=p_id).first()
        flash("Payment Done Successfully!!")
    return render_template("final_billing.html", patient=patient, med_is=med_is, meds=meds, tests=tests, test_is=test_is, data=data, username=session.get("username"))