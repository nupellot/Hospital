import os
from typing import Optional, Dict

from flask import (
    Blueprint, request,
    render_template, current_app,
    session, redirect, url_for
)

from access import login_required
from database.operations import select_dict
from database.sql_provider import SQLProvider


blueprint_person = Blueprint('bp_person', __name__, template_folder='templates', static_folder="static")
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


# Обрабатываем страницу с информацией о пользователе.
@blueprint_person.route('/<string:user_login>', methods=['GET', 'POST'])
# @login_required
def person(user_login):
    # return blueprint_patient.static_folder
    # if user_login != session["login"]:
    #     return "Отказано в доступе"

    if request.method == 'GET':
        return render_patient(user_login)
        # sql_for_stories = provider.get("stories.sql", login=user_login)
        # print("sql_for_stories:", sql_for_stories)
        # stories = select_dict(current_app.config['db_config'], sql_for_stories)
        # print("stories:", stories)
        #
        # if session["role"] == "patient":
        #     sql_for_location = provider.get("location.sql", id_patient=session["id_patient"])
        #     location = select_dict(current_app.config['db_config'], sql_for_location)
        #     print("location:", location)
        #     if location:
        #         location = location[0]  # Человек может находиться только в одной палате одновременно.
        #         session["location"] = str(location["id_department"]) + "-" + str(location["id_ward"])
        #
        return "Kek"
        # return render_template('person.html', session=session, stories=stories)
    else:
        return "LOL KEK ERROR"


# Обрабатываем страницу с информаций о пациенте.
def render_patient(user_login):
    # Получаем информацию о текущем пациенте.
    sql_for_patient = provider.get("patient.sql", login=user_login)
    print("sql_for_patient:", sql_for_patient)
    patient = select_dict(current_app.config['db_config'], sql_for_patient)
    print("patient:", patient)

    # Получаем информацию обо всех историях болезни текущего пациента.
    sql_for_patient_stories = provider.get("patient_stories.sql", login=user_login)
    print("sql_for_patient_stories:", sql_for_patient_stories)
    patient_stories = select_dict(current_app.config['db_config'], sql_for_patient_stories)
    print("patient_stories:", patient_stories)

    # Получаем информацию обо всех осмотрах текущего пациента.
    sql_for_patient_surveys = provider.get("patient_surveys.sql", login=user_login)
    print("sql_for_patient_surveys:", sql_for_patient_surveys)
    patient_surveys = select_dict(current_app.config['db_config'], sql_for_patient_surveys)
    print("patient_surveys:", patient_surveys)

    # Превращаем массив пациентов в одного пациента.
    if len(patient) != 1:
        return "You have multiple patients with the same login!"
    else:
        patient = patient[0]

    # Хитро склеиваем все предыдущие результаты в единый словарь.
    patient["stories"] = []
    for story in patient_stories:
        story["surveys"] = []
        for survey in patient_surveys:
            if story["id_story"] == survey["survey_story"]:
                story["surveys"].append(survey)
        patient["stories"].append(story)

    # Добавляем к данным о пациенте информацию о его местонахождении.
    sql_for_location = provider.get("location.sql", id_patient=patient["id_patient"])
    location = select_dict(current_app.config['db_config'], sql_for_location)
    print("location:", location)
    if location:
        if len(location) != 1:
            return "This patient is in two locations simultaneously"
        location = location[0]  # Человек может находиться только в одной палате одновременно.
        patient["location"] = str(location["id_department"]) + "-" + str(location["id_ward"])

    # Добавляем к данным о пациенте его фотографию.
    patient["image"] = url_for("static", filename="user_photos") + "/" + patient["image"]

    for story in patient["stories"]:
        # Добавляем к данным об историях фото лечащих врачей.
        story["image"] = url_for("static", filename="user_photos") + "/" + story["image"]
        # Добавляем к данным о пациенте информацию о его местонахождении.
        story["location"] = str(story["id_department"]) + "-" + str(story["id_ward"])

    # Для единообразия фронтенда добавляем пациенту роль.
    patient["role"] = "patient"

    print("patient: ", patient)

    return render_template('patient.html', session=session, person=patient, patient=patient)


# Обрабатываем страницу настроек.
@blueprint_person.route('/<string:user_login>/settings', methods=['GET', 'POST'])
def settings(user_login):
    if request.method == 'GET':
        # Получаем информацию о текущем пациенте.
        sql_for_patient = provider.get("patient.sql", login=user_login)
        # print("sql_for_patient:", sql_for_patient)
        patient = select_dict(current_app.config['db_config'], sql_for_patient)
        # print("patient:", patient)

        # Превращаем массив пациентов в одного пациента.
        if len(patient) != 1:
            return "You have multiple patients with the same login!"
        else:
            patient = patient[0]

        # Добавляем к данным о пациенте информацию о его местонахождении.
        sql_for_location = provider.get("location.sql", id_patient=patient["id_patient"])
        location = select_dict(current_app.config['db_config'], sql_for_location)
        print("location:", location)
        if location:
            if len(location) != 1:
                return "This patient is in two locations simultaneously"
            location = location[0]  # Человек может находиться только в одной палате одновременно.
            patient["location"] = str(location["id_department"]) + "-" + str(location["id_ward"])

        # Добавляем к данным о пациенте его фотографию.
        patient["image"] = url_for("static", filename="user_photos") + "/" + patient["image"]

        # Для единообразия фронтенда добавляем пациенту роль.
        patient["role"] = "patient"

        return render_template('settings.html', session=session, person=patient)
    else:
        return "LOL KEK ERROR"


