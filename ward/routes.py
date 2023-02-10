import os
from typing import Optional, Dict

from flask import (
    Blueprint, request,
    render_template, current_app,
    session, redirect, url_for
)

from database.operations import select_dict, select
from database.sql_provider import SQLProvider


blueprint_ward = Blueprint('bp_ward', __name__, template_folder='templates', static_folder='static')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


# Обрабатываем страницу с информацией о пользователе.
@blueprint_ward.route('/<int:department_id>-<int:ward_id>', methods=['GET', 'POST'])
def specific_ward(department_id, ward_id):
    if session["login"] == "patient":
        return "Отказано в доступе"

    if request.method == 'GET':
        sql_for_ward = provider.get("ward.sql", id_ward=ward_id, id_department=department_id)
        # print("sql_for_stories:", sql_for_stories)
        ward = select_dict(current_app.config['db_config'], sql_for_ward)
        # print("ward:", ward)
        if ward:
            ward = ward[0]
            sql_for_occupancy = provider.get("occupancy.sql", id_ward=ward_id, id_department=department_id)
            ward["occupancy"] = select_dict(current_app.config['db_config'], sql_for_occupancy)[0]["amount"]


# ward["occupancy"]
        # print("ward:", ward)
        # return "kek"
        # if session["role"] == "patient":
        #     sql_for_location = provider.get("location.sql", id_patient=session["id_patient"])
        #     location = select_dict(current_app.config['db_config'], sql_for_location)
        #     print("location:", location)
        #     if location:
        #         location = location[0]  # Человек может находиться только в одной палате одновременно.
        #         session["location"] = str(location["id_department"]) + "-" + str(location["id_ward"])

        return render_template('ward.html', ward=ward, session=session)
    else:
        return "LOL KEK ERROR"


# # Обрабатываем страницу с информацией о конкретной палате.
# @blueprint_ward.route('/<int:department_id>-<int:ward_id>', methods=['GET', 'POST'])
# def specific_ward(department_id, ward_id):
#     return "lol"
#     # if user_login != session["login"]:
#     #     return "Отказано в доступе"
#     #
#     # if request.method == 'GET':
#     #     sql_for_stories = provider.get("stories.sql", login=user_login)
#     #     # print("sql_for_stories:", sql_for_stories)
#     #     stories = select_dict(current_app.config['db_config'], sql_for_stories)
#     #     print("stories:", stories)
#     #
#     #     if session["role"] == "patient":
#     #         sql_for_location = provider.get("location.sql", id_patient=session["id_patient"])
#     #         location = select_dict(current_app.config['db_config'], sql_for_location)
#     #         print("location:", location)
#     #         if location:
#     #             location = location[0]  # Человек может находиться только в одной палате одновременно.
#     #             session["location"] = str(location["id_department"]) + "-" + str(location["id_ward"])
#     #
#     #     return render_template('patient.html', session=session, stories=stories)
#     # else:
#     #     return "LOL KEK ERROR"







