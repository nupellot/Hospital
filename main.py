import json
import os

from flask import Flask, render_template, session, request, redirect, url_for, current_app
from auth.routes import blueprint_auth
from database.connection import UseDatabase
from database.operations import select_dict
from database.sql_provider import SQLProvider
from access import login_required
from person.routes import blueprint_person
from ward.routes import blueprint_ward

app = Flask(__name__, template_folder='templates', static_folder="static")
app.secret_key = 'SuperKey'

app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_person, url_prefix="/person")
app.register_blueprint(blueprint_ward, url_prefix='/ward')

app.config['access_config'] = json.load(open('configs/access.json'))
app.config['cache_config'] = json.load(open('configs/cache.json'))
app.config['db_config'] = json.load(open('configs/db.json'))

for key in app.config['db_config']:
    app.config['db_config'][key] = os.getenv(str(app.config['db_config'][key]))
    print(app.config['db_config'][key])
# app.config['db_config']['password'] = os.getenv('MYSQLPASSWORD')


provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@app.route('/', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == "GET":
        if session["role"] == "doctor":
            return render_doctor()
        if session["role"] == "registrator":
            return render_registrator()
        else:
            return redirect(url_for("bp_person.person", user_login=session["login"]))

    if request.method == "POST":
        # print("request.form", request.form)
        if session["role"] == "doctor":
            return process_doctor()
        if session["role"] == "registrator":
            return process_registrator()
        else:
            return "Функционал для роли " + session["role"] + " не определен"
    else:
        return "Unknown request.method"


def process_doctor():
    if request.form.get("is-survey-form") == "yes":
        # print("request.form.get(\"id_patient\"):", request.form.get("id_patient"))
        survey_patient = request.form.get("id_patient")
        # print("request.form.get(\"survey_text\"):", request.form.get("survey_text"))
        prescriptions = request.form.get("survey_text")
        sql_for_get_story_by_patient = provider.get("get_story_by_patient_id.sql",
                                                    patient_id=survey_patient)
        survey_story = select_dict(current_app.config['db_config'], sql_for_get_story_by_patient)
        survey_story_id = survey_story[0]["id_story"]
        sql_for_new_survey = provider.get("new_survey.sql",
                                          prescriptions=prescriptions,
                                          survey_doctor=session["id_doctor"],
                                          survey_story=survey_story_id)

        with UseDatabase(current_app.config['db_config']) as cursor:
            cursor.execute(sql_for_new_survey)

    if request.form.get("is-discharge-form") == "yes":
        sql_for_discharge_patient = provider.get("discharge_patient.sql",
                                                 patient_id=request.form.get("id_patient"))
        with UseDatabase(current_app.config['db_config']) as cursor:
            print("sql_for_discharge_patient:", sql_for_discharge_patient)
            cursor.execute(sql_for_discharge_patient)

    return render_doctor()


def render_doctor():
    # Получаем информацию обо всех пациентах, которые сейчас лежат в госпитале.
    sql_for_active_patients = provider.get("active_patients.sql")
    # print("sql_for_active_patients:", sql_for_active_patients)
    active_patients = select_dict(current_app.config['db_config'], sql_for_active_patients)
    # print("active_patients:", active_patients)

    # Получаем информацию обо всех пациентах данного врача, которые сейчас лежат в госпитале.
    sql_for_doctor_active_patients = provider.get("doctor_active_patients.sql", id_doctor=session["id_doctor"])
    # print("sql_for_doctor_active_patients:", sql_for_doctor_active_patients)
    doctor_active_patients = select_dict(current_app.config['db_config'], sql_for_doctor_active_patients)
    # print("doctor_active_patients:", doctor_active_patients)

    for patient in doctor_active_patients:
        patient["location"] = str(patient["id_department"]) + "-" + str(patient["id_ward"])
        patient["image"] = url_for("static", filename="user_photos") + "/" + patient["image"]

    return render_template('dashboard.html',
                           active_patients=active_patients,
                           doctor_active_patients=doctor_active_patients,
                           session=session)


def process_registrator():
    if request.form.get("is-new-story-form") == "yes":
        print("request.form", request.form)
        # print("request.form.get(\"id_patient\"):", request.form.get("id_patient"))
        # survey_patient = request.form.get("id_patient")
        # # print("request.form.get(\"survey_text\"):", request.form.get("survey_text"))
        # prescriptions = request.form.get("survey_text")
        # sql_for_get_story_by_patient = provider.get("get_story_by_patient_id.sql",
        #                                             patient_id=survey_patient)
        # survey_story = select_dict(current_app.config['db_config'], sql_for_get_story_by_patient)
        # survey_story_id = survey_story[0]["id_story"]
        sql_for_new_story = provider.get("new_story.sql",
                                        diagnosis=request.form.get("diagnosis"),
                                        story_doctor=request.form.get("id_doctor"),
                                        story_ward=request.form.get("id_ward"),
                                        story_patient=request.form.get("id_patient")
                                        )

        with UseDatabase(current_app.config['db_config']) as cursor:
            print("sql_for_new_story", sql_for_new_story)
            cursor.execute(sql_for_new_story)


    return render_registrator()


def render_registrator():
    # Получаем информацию обо всех пациентах.
    sql_for_inactive_patients = provider.get("inactive_patients.sql")
    # print("sql_for_inactive_patients:", sql_for_inactive_patients)
    inactive_patients = select_dict(current_app.config['db_config'], sql_for_inactive_patients)
    # print("inactive_patients:", inactive_patients)

    # Получаем информацию обо всех палатах.
    sql_for_all_wards = provider.get("all_wards.sql")
    # print("sql_for_all_wards:", sql_for_all_wards)
    all_wards = select_dict(current_app.config['db_config'], sql_for_all_wards)
    # print("all_wards:", all_wards)
    
    # Получаем информацию о занятости всех палат.
    sql_for_all_wards_occupancy = provider.get("all_wards_occupancy.sql")
    # print("sql_for_all_wards_occupancy:", sql_for_all_wards_occupancy)
    all_wards_occupancy = select_dict(current_app.config['db_config'], sql_for_all_wards_occupancy)
    # print("all_wards_occupancy:", all_wards_occupancy)

    # Склеиваем палаты с их занятостью.
    for ward in all_wards:
        for occupancy in all_wards_occupancy:
            if ward["id_ward"] == occupancy["id_ward"]:
                ward["occupancy"] = occupancy["occupancy"]
    # print("all_wards:", all_wards)
    
    # Получаем информацию обо всех врачах.
    sql_for_all_doctors = provider.get("all_doctors.sql")
    # print("sql_for_all_doctors:", sql_for_all_doctors)
    all_doctors = select_dict(current_app.config['db_config'], sql_for_all_doctors)
    # print("all_doctors:", all_doctors)

    # Получаем информацию о занятости всех палат.
    sql_for_all_doctors_occupancy = provider.get("all_doctors_occupancy.sql")
    # print("sql_for_all_doctors_occupancy:", sql_for_all_doctors_occupancy)
    all_doctors_occupancy = select_dict(current_app.config['db_config'], sql_for_all_doctors_occupancy)
    # print("all_doctors_occupancy:", all_doctors_occupancy)

    # Склеиваем палаты с их занятостью.
    for doctor in all_doctors:
        for occupancy in all_doctors_occupancy:
            if doctor["id_doctor"] == occupancy["id_doctor"]:
                doctor["occupancy"] = occupancy["occupancy"]
    # print("all_doctors:", all_doctors)

    return render_template('dashboard.html',
                           patients=inactive_patients,
                           session=session,
                           doctors=all_doctors,
                           wards=all_wards)


@app.route('/exit')
@login_required
def exit_func():
    session.clear()
    return render_template('exit.html')


# @app.route('/<string:user_login>/settings')
# def settings(user_login):
#     if request.method == 'GET':
#         return render_template('settings.html', session=session)
#     else:
#         return "LOL KEK ERROR"


if __name__ == '__main__':
    # app = add_blueprint_access_handler(app, ['blueprint_report'], group_required)
    # app = add_blueprint_access_handler(app, ['blueprint_market'], external_required)
    app.run(host='0.0.0.0', port=5002, debug=True)
