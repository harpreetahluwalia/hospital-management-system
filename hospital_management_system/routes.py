from flask import render_template, request, redirect, flash, session
from hospital_management_system.models import User
from hospital_management_system import app, db

@app.route('/')
def home():
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

# @app.route('/signup')
# def signup():
#     admin = User(user_id=1, username="admin", password="admin")
#     db.session.add(admin)
#     db.session.commit()
#     return "abc"

# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html')





    