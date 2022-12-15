import os
from typing import Optional, Dict

from flask import (
    Blueprint, request,
    render_template, current_app,
    session, redirect, url_for
)

from database.operations import select
from database.operations import select_dict
from database.sql_provider import SQLProvider

##### СОЗДАНИЕ BLUEPRINT'а #####
# 'admin' – имя Blueprint, которое будет суффиксом ко всем именам методов, данного модуля;
# __name__ – имя исполняемого модуля, относительно которого будет искаться папка admin и соответствующие подкаталоги;
# template_folder – подкаталог для шаблонов данного Blueprint (необязательный параметр, при его отсутствии берется подкаталог шаблонов приложения);
# static_folder – подкаталог для статических файлов (необязательный параметр, при его отсутствии берется подкаталог static приложения).
# После создания эскиза его нужно зарегистрировать в основном приложении.
blueprint_auth = Blueprint('bp_auth', __name__, template_folder='templates', static_folder='static')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


# Судя по всему - некоторый встроенный декоратор flask'a с заранее предусмотренными аргументами.
@blueprint_auth.route('/', methods=['GET', 'POST'])
def start_auth():
    if request.method == 'GET':
        return render_template('input_login.html', message='')
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        # if request.form.get("is-doctor"):
        #     is_doctor = True
        # else:
        #     is_doctor = False
        print("login", login)
        print("password", password)
        if login:
            # Получаем информацию о разных пользователях с таким логином и паролем.
            user_info = get_user_info(login, password)
            print("user_info", user_info)
            if user_info:
                # Берём первого (единственного) пользователя с таким логином и паролем.
                user_dict = user_info[0]
                print("user_info[0]", user_info[0])
                # Записываем в сессию полученную из БД информацию о пользователе.
                session.clear()

                session["role"] = "patient"
                for field in user_dict:
                    if user_dict[field] == None:
                        session[field] = ""
                    else:
                        session[field] = user_dict[field]

                if session["image"]:
                    session["image"] = url_for("static", filename="user_photos") + "/" + session["image"]
                # session['user_id'] = user_dict['user_id']
                # session['user_group'] = user_dict['user_group']
                # session['user_name'] = user_dict['user_name']
                # session['user_login'] = login
                session.permanent = True
                return redirect(url_for('bp_settings.main', user_login = session["login"]))
            else:  # Не нашёлся пользователь с такими данными.
                return render_template('input_login.html', message='Неверные данные для входа')
        return render_template('input_login.html', message='Повторите ввод')


# В случае нахождения юзера с такими данными возвращает лист словарей.
# Каждый словарь - набор информации о конкретном пользователе.
def get_user_info(login: str, password: str) -> Optional[Dict]:
    # Создаём sql-запросы для получения информации о польователях из БД.
    # if is_doctor:
    #     sql_query = provider.get('doctor.sql', login=login, password=password)
    # if not is_doctor:
    #     sql_query = provider.get('patient.sql', login=login, password=password)

    sql_query = provider.get('doctor.sql', login=login, password=password)
    user_info = select_dict(current_app.config['db_config'], sql_query)
    if user_info:
        return user_info
    elif not user_info:
        sql_query = provider.get('patient.sql', login=login, password=password)
        user_info = select_dict(current_app.config['db_config'], sql_query)
        return user_info


    # Выполняем нужный sql-запрос.
    # user_info = select_dict(current_app.config['db_config'], sql_query)
    # if user_info:
    #     return user_info
    # else:
    #     return None

    # Получили готовые запросы.
    # print(sql_for_doctors)
    # user_info = None
    #
    # for sql_search in [sql_internal, sql_external]:
    #     # Выполняем готовые запросы. Каждый раз получаем строку с информацией об одном из пользователей в БД.
    #     _user_info = select_dict(current_app.config['db_config'], sql_search)
    #     if _user_info:  # Если в БД нашёлся такой пользователь с такими данными.
    #         # print('Congratulations ', _user_info)
    #         user_info = _user_info
    #         del _user_info
    #         break
    #     # print(user_info)
    # return user_info
