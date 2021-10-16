from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy.sql.functions import user
from .models import  User, Employer
from werkzeug.security import check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import json

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_email = request.form.get('login_email')
        password = request.form.get('password')
        employer_id = request.form.get('employer_id')

        user = Employer.query.filter_by(login_email=login_email).first()
        if user:
            if user.password==password and employer_id == user.employer_id:
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home', page_num = user.id))
            elif password != user.password:
                flash('Incorrect password, try again.', category='error')
            else:
                flash('Incorrect Employer ID.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/', methods=['GET', 'POST'])
def bookingAppointment():
    if request.method == 'POST':
        email = request.form.get('email')
        full_name = request.form.get('fullName')
        age = request.form.get('age')
        phone_number = request.form.get('phone_number')
        NRIC = request.form.get('NRIC')
        date_pick = request.form.get('dateGet')
        gender = request.form.get('Gender')

        symptoms = json.dumps(list(map(int, request.form.getlist('customCheckbox'))))
        next_symptoms = symptoms.replace("[","")
        symptom = next_symptoms.replace("]","")
        datetime_pick = User.query.filter_by(date_pick=date_pick).first()

        if len(email) < 4:
            flash('Email must be greater than 3 characters.Please fill the form again', category='error')
        elif len(full_name) < 4:
            flash('Full name must be greater than 4 character.Please fill the form again', category='error')
        elif len(phone_number) < 8:
            flash('Password must be at least 8 characters.Please fill the form again', category='error')
        elif len(NRIC) <= 6 :
            flash('NRIC/Birth Cert must equal to 7. Please fill the form again', category='error')
        elif datetime_pick:
            flash('The datetime already choosing by others. Please fill the form again and choosing another day', category='error')
        elif len(date_pick) < 1:
            flash('Datetime can not be blanks', category='error')
        else:
            new_user = User(email=email, full_name=full_name, age=age, gender=gender, phone_number=phone_number, NRIC=NRIC, date_pick=date_pick, SymptomsResult=symptom)
            db.session.add(new_user)
            db.session.commit()
            flash('Successful booking healthcare time, your information would be save. Please prepare datetime for your health checking day', category='success')
            return redirect(url_for('auth.bookingAppointment'))

    return render_template("bookingAppointment.html", user=current_user)
