from typing import List

from database.connection import UseDatabase


# Возвращает результат (набор строк) выполнения sql-запроса к бд, подключенной по db_config
# В виде словаря.
def select_dict(db_config: dict, sql: str) -> dict:
    result = []
    with UseDatabase(db_config) as cursor:

        if cursor is None:
            raise ValueError('Курсор не создан')

        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]

        for row in cursor.fetchall():
            result.append(dict(zip(schema, row)))
    # print(f"result_dict: {result}")
    return result


# Возвращает результат выполнения sql-запроса в виде двух листов - заголовка и содержимого.
def select(dbconfig: dict, _sql: str):
    with UseDatabase(dbconfig) as cursor:

        if cursor is None:
            raise ValueError('Курсор не создан')

        cursor.execute(_sql)
        # schema - заголовки результирующей таблицы.
        schema = [column[0] for column in cursor.description]
        # result - Все остальные строки результирующей таблицы.
        result = cursor.fetchall()
    # print("select")
    # print(result)
    # print(schema)
    return result, schema


def call_proc(dbconfig: dict, proc_name: str, *args):
    with UseDatabase(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        param_tuple = []
        for arg in args:
            param_tuple.append(arg)
        # param_tuple = tuple(param_tuple)
        print("tuple: ", param_tuple)
        print("proc_name", proc_name)
        res = cursor.callproc(proc_name, param_tuple)
        # print("res: ", res)
    return res
