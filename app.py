import json
import os

from flask import Flask, render_template, session, request, redirect, url_for, current_app
from auth.routes import blueprint_auth
from catalog.routes import blueprint_catalog
from database.connection import UseDatabase
from database.operations import select_dict
from database.sql_provider import SQLProvider
from market.routes import blueprint_market
from orderlist.routes import blueprint_orderlist
from report.routes import blueprint_report
from basket.routes import blueprint_basket
from access import login_required
from person.routes import blueprint_person
from ward.routes import blueprint_ward

app = Flask(__name__, template_folder='templates', static_folder="static")
app.secret_key = 'SuperKey'

app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_market, url_prefix='/market')
app.register_blueprint(blueprint_basket, url_prefix='/basket')
app.register_blueprint(blueprint_catalog, url_prefix='/catalog')
app.register_blueprint(blueprint_orderlist, url_prefix='/orderlist')
app.register_blueprint(blueprint_person, url_prefix="/person")
app.register_blueprint(blueprint_ward, url_prefix='/ward')


app.config['db_config'] = json.load(open('configs/db.json'))
app.config['access_config'] = json.load(open('configs/access.json'))
app.config['cache_config'] = json.load(open('configs/cache.json'))


provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@app.route('/', methods=['GET', 'POST'])
# @login_required
def menu_choice():
    if request.method == "GET":
        if session["role"] == "doctor":
            # Получаем информацию обо всех пациентах, которые сейчас лежат в госпитале.
            sql_for_active_patients = provider.get("active_patients.sql")
            # print("sql_for_active_patients:", sql_for_active_patients)
            active_patients = select_dict(current_app.config['db_config'], sql_for_active_patients)
            print("active_patients:", active_patients)

            return render_template('dashboard.html', patients=active_patients, session=session)
        else:
            return redirect(url_for("bp_person.person", user_login=session["login"]))
    if request.method == "POST":
        if session["role"] == "doctor":
            print("request.form.get(\"id_patient\"):", request.form.get("id_patient"))
            survey_patient = request.form.get("id_patient")
            print("request.form.get(\"survey_text\"):", request.form.get("survey_text"))
            prescriptions = request.form.get("survey_text")

            sql_for_get_story_by_patient = provider.get("get_story_by_patient_id.sql", patient_id=survey_patient)
            survey_story = select_dict(current_app.config['db_config'], sql_for_get_story_by_patient)
            survey_story_id = survey_story[0]["id_story"]

            sql_for_new_survey = provider.get("new_survey.sql",
                                              prescriptions=prescriptions,
                                              survey_doctor=session["id_doctor"],
                                              survey_story=survey_story_id)


            print("sql_for_new_survey:", sql_for_new_survey)

            with UseDatabase(current_app.config['db_config']) as cursor:
                cursor.execute(sql_for_new_survey)


        return "KEk"
    else:
        return "Unknown request.method"
    # return render_template("base.html", session=session, request=request)
    # if session.get('user_group', None):
    #     return render_template('internal_user_menu.html', session=session, request=request)
    # return render_template('external_user_menu.html')


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
    app.run(host='127.0.0.1', port=5001, debug=True)