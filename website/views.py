import flask
from flask.globals import session
from matplotlib.figure import Figure
from .models import Cancel, User
from flask import Blueprint, app, render_template, request, flash, redirect, url_for, send_file, Response
from flask_login import login_required
from . import db
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import json

views = Blueprint('views', __name__)

@views.route('/home/<int:page_num>', methods=['GET', 'POST'])
@login_required
def home(page_num):
    user = User.query.paginate(per_page=5, page=page_num, error_out=True)
    return render_template("home.html", user = user)


# Prediction System

plt.rcParams["figure.figsize"] = [8, 5]
plt.rcParams["figure.autolayout"] = True

@views.route('/prediction/<int:id>/', methods=['GET', 'POST'])
def prediction(id):
    # if request.method == 'GET':
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        xs = ['heart','gastrointestinal', 'diabetes', 'infection', 'stroke', 'cancer', 'liver', 'thyroid', 'mental']
        # user = User.query.get(3)
        user = User.query.get_or_404(id)
        if user.SymptomsResult == 0 or user.SymptomsResult is None:
            ys = [0,0,0,0,0,0,0,0,0]
        else:
            symptoms = list(user.SymptomsResult.split(" "))
            x1 = 0
            x2 = 0
            x3 = 0
            x4 = 0
            x5 = 0
            x6 = 0
            x7 = 0
            x8 = 0
            x9 = 0
            for symptom in range(len(symptoms)):
                ys = [x1,x2,x3,x4,x5,x6,x7,x8,x9]
                if symptoms[symptom] == "1,":
                    x1 += 10
                elif symptoms[symptom] == "2,":
                    x2 += 10
                    x6 += 10
                elif symptoms[symptom] == "3,":
                    x1 += 10
                    x3 += 10
                    x8 += 10
                elif symptoms[symptom] == "4,":
                    x8 += 10
                elif symptoms[symptom] == "5,":
                    x1 += 10
                    x3 += 10
                elif symptoms[symptom] == "6,":
                    x1 += 10
                elif symptoms[symptom] == "7,":
                    x2 += 10
                elif symptoms[symptom] == "8,":
                    x6 += 10
                elif symptoms[symptom] == "9,":
                    x1 += 10
                    x4 += 10
                    x7 += 10
                elif symptoms[symptom] == "10,":
                    x7 += 10
                elif symptoms[symptom] == "11,":
                    x4 += 10
                    x6 += 10
                elif symptoms[symptom] == "12,":
                    x5 += 10
                else :
                    x9 += 10
        axis.plot(xs, ys, color='red', linestyle='--')
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')

# End Prediction System

#insert data to mysql database via html forms
@views.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
        email = request.form.get('email')
        full_name = request.form.get('fullName')
        age = request.form.get('age')
        gender = request.form.get('Gender')
        phone_number = request.form.get('phone_number')
        NRIC = request.form.get('NRIC')
        date_pick = request.form.get('dateGet')
        new_user = User(email=email, full_name=full_name, age=age, gender=gender, phone_number=phone_number, NRIC=NRIC, date_pick=date_pick)
        db.session.add(new_user)
        db.session.commit()
        flash("New Booking Inserted Successfully", category='success')
        return redirect(url_for('views.home'))
    return render_template("home.html")

#update employee
@views.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        user = User.query.get(request.form.get('id'))
        user.email = request.form['email']
        user.full_name = request.form['full_name']
        user.age = request.form['age']
        user.gender = request.form['Gender']
        user.phone_number = request.form['phone_number']
        user.NRIC = request.form['NRIC']
        user.date_pick = request.form['date_pick']
        datetime_pick = User.query.filter_by(date_pick=user.date_pick).first()
        if user.date_pick == datetime_pick:
            flash('The datetime already choosing by others', category='error')
        else:
            db.session.commit()
            flash("User Booking Updated Successfully")
        return redirect(url_for('views.changeAppointment'))

#delete employee
@views.route('/delete/<int:id>/', methods = ['GET', 'POST'])
def delete(id):
    user = User.query.get_or_404(id)
    reason = request.form.get('reason')
    remarks = request.form.get('remarks')
    new_notes = Cancel(reason = reason, remarks = remarks)
    try:
        db.session.add(new_notes)
        db.session.delete(user)
        db.session.commit()
        flash("User Deleted Successfully")
        return redirect(url_for('views.changeAppointment'))
    except:
        flash("Whoops ! Deleted not successful")

#Search
@views.route('/changeappointment', methods = ['GET', 'POST'])
def changeAppointment():
    user = User.query.order_by(User.id.asc())
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        if len(tag) >= 6:
            search = "%{}%".format(tag)
            user = User.query.filter(User.NRIC.like(search)).paginate()
            return render_template('changeAppointment.html', user=user, tag=tag)
        else:
            flash('The NRIC can not below 7 characters', category='error')
    return render_template('changeAppointment.html', user=user)





