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


# Обрабатываем страницу с информацией о конкретной палате.
@blueprint_ward.route('/<int:department_id>-<int:ward_id>', methods=['GET', 'POST'])
def specific_ward(department_id, ward_id):
    # if session["role"] == "patient":
    #     return "Отказано в доступе"

    if request.method == 'GET':
        sql_for_ward = provider.get("ward.sql", id_ward=ward_id, id_department=department_id)
        # print("sql_for_stories:", sql_for_stories)
        ward = select_dict(current_app.config['db_config'], sql_for_ward)
        print("ward:", ward)
        if ward:
            # ward = ward[0]
            sql_for_occupancy = provider.get("occupancy.sql", id_ward=ward_id, id_department=department_id)
            # print("kek", select_dict(current_app.config['db_config'], sql_for_occupancy))
            ward[0]["occupancy"] = select_dict(current_app.config['db_config'], sql_for_occupancy)[0]["amount"]

        # Исправляем адреса для аватарок.
        for patient in ward:
            patient["image"] = url_for("static", filename="user_photos/" + patient["image"])
        print("ward:", ward)

        return render_template('ward.html', ward=ward, session=session)
    else:
        return "LOL KEK ERROR"


# Обрабатываем страницу с информацией о всех палатах
@blueprint_ward.route('/', methods=['GET', 'POST'])
def wards_list():
    if session["login"] == "patient":
        return "Отказано в доступе"

    if request.method == 'GET':
        # Запрос, в котором мы получаем информацию о заполненности всех отделений.
        sql_for_departments_occupancy = provider.get("departments_occupancy.sql")
        # print("sql_for_stories:", sql_for_stories)
        departments_occupancy = select_dict(current_app.config['db_config'], sql_for_departments_occupancy)
        # print("departments_occupancy:", departments_occupancy)

        # Запрос, в котором мы получаем информацию о заполненности всех палат.
        sql_for_wards_occupancy = provider.get("wards_occupancy.sql")
        # print("sql_for_stories:", sql_for_stories)
        wards_occupancy = select_dict(current_app.config['db_config'], sql_for_wards_occupancy)
        # print("wards_occupancy:", wards_occupancy)
        
        # Запрос, в котором мы получаем информацию о главах каждого отделения.
        sql_for_departments_heads = provider.get("departments_heads.sql")
        # print("sql_for_stories:", sql_for_stories)
        departments_heads = select_dict(current_app.config['db_config'], sql_for_departments_heads)
        # print("departments_heads:", departments_heads)
        
        # Запрос, в котором мы получаем информацию о врачах каждого отделения.
        sql_for_departments_doctors = provider.get("departments_doctors.sql")
        # print("sql_for_stories:", sql_for_stories)
        departments_doctors = select_dict(current_app.config['db_config'], sql_for_departments_doctors)
        # print("departments_doctors:", departments_doctors)

        # Теперь хитро склеиваем все предыдущие результаты для того, чтобы передать всё на фронт одной переменной.
        departments = departments_occupancy
        for department in departments:
            # Приклеиваем информацию о палатах.
            department["wards"] = []
            for ward in wards_occupancy:
                if ward["id_department"] == department["id_department"]:
                    if not ward["ward_occupancy"]:  # Избавляемся от надписи None для пустых палат.
                        ward["ward_occupancy"] = 0
                    department["wards"].append(ward)
            # Приклеиваем информацию о главе департамента.
            for doctor in departments_doctors:
                if doctor["id_department"] == department["id_department"]:
                    department["department_head"] = doctor
            # Приклеиваем информацию о врачах отделения.
            department["doctors"] = []
            for doctor in departments_doctors:
                if doctor["id_department"] == department["id_department"]:
                    department["doctors"].append(doctor)

        # print("departments:", departments)

    return render_template('all_wards.html', departments=departments, session=session)









