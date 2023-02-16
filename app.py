import json

from flask import Flask, render_template, session, request, redirect, url_for
from auth.routes import blueprint_auth
from catalog.routes import blueprint_catalog
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


@app.route('/', methods=['GET', 'POST'])
@login_required
def menu_choice():
    return redirect(url_for("bp_person.person", user_login=session["login"]))
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