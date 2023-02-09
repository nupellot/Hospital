from functools import wraps

from flask import session, render_template, current_app, request, redirect, url_for


# Проверка на то, прошёл ли юзер авторизацию.
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        return redirect(url_for('bp_auth.start_auth'))
    return wrapper


def group_validation(config: dict) -> bool:
    endpoint_app = request.endpoint.split('.')[0]
    # session - словарь, в который мы сами можем добавлять элементы.
    if 'user_group' in session:  # Если мы добавили элемент 'user_group' в сессию.
        user_group = session['user_group']
        if user_group in config and endpoint_app in config[user_group]:
            # Если у нужной группы есть доступ к нужному модулю.
            return True
    return False


def group_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        config = current_app.config['access_config']
        if group_validation(config):
            return f(*args, **kwargs)
        return render_template('exceptions/internal_only.html')
    return wrapper


def external_validation(config):
    # endpoint_app - обработчик, из которого вызван реквест.
    # Метод split разбивает строку на подстроки, находя разделитель в виде своего аргумента.
    endpoint_app = request.endpoint.split('.')[0]
    user_id = session.get('user_id', None)
    user_group = session.get('user_group', None)
    if user_id and user_group is None:
        # Сравним обработчик с данными из access.
        if endpoint_app in config['external']:
            return True
    return False


# Проверка на то, является ли текущий юзер внешним.
def external_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        config = current_app.config['access_config']
        if external_validation(config):
            return f(*args, **kwargs)
        return render_template('exceptions/external_only.html')
    return wrapper