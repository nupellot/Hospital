import os
from typing import Optional, Dict

from flask import (
    Blueprint, request,
    render_template, current_app,
    session, redirect, url_for
)

from database.operations import select_dict
from database.sql_provider import SQLProvider


blueprint_patient = Blueprint('bp_patient', __name__, template_folder='templates', static_folder='static')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


# Обрабатываем страницу с информацией о пользователе.
@blueprint_patient.route('/<string:user_login>', methods=['GET', 'POST'])
def main(user_login):
    if user_login != session["login"]:
        return "Отказано в доступе"

    if request.method == 'GET':
        sql_for_stories = provider.get("stories.sql", login=user_login)
        # print("sql_for_stories:", sql_for_stories)
        stories = select_dict(current_app.config['db_config'], sql_for_stories)
        print("stories:", stories)

        if session["role"] == "patient":
            sql_for_location = provider.get("location.sql", id_patient=session["id_patient"])
            location = select_dict(current_app.config['db_config'], sql_for_location)
            print("location:", location)
            if location:
                location = location[0]  # Человек может находиться только в одной палате одновременно.
                session["location"] = str(location["id_department"]) + "-" + str(location["id_ward"])

        return render_template('patient.html', session=session, stories=stories)
    else:
        return "LOL KEK ERROR"


# Обрабатываем страницу настроек.
@blueprint_patient.route('/<string:user_login>/settings', methods=['GET', 'POST'])
def settings(user_login):
    if request.method == 'GET':
        return render_template('settings.html', session=session)
    else:
        return "LOL KEK ERROR"


