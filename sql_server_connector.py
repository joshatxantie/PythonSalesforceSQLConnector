import json

import pyodbc
from sqlalchemy import create_engine, event
import urllib

from urllib import parse

credentials = json.load(open('credentials.json'))

server = credentials['server']
database = credentials['database']
username = credentials['sql_username']
password = credentials['sql_password']
driver = '{ODBC Driver 17 for SQL Server}'
# def get_connection_for_sql_server(server, database, username, password):
#     connection = pyodbc.connect(
#         'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';PORT=1433;DATABASE=' + database
#         + ';UID=' + username + ';PWD=' + password)
#     return connection


def get_engine_for_sql_server():
    params = parse.quote_plus(
        'Driver=%s;' % driver +
        'Server=tcp:%s,1433;' % server +
        'Database=%s;' % database +
        'Uid=%s;' % username +
        'Pwd={%s};' % password +
        'Encrypt=yes;' +
        'TrustServerCertificate=no;' +
        'Connection Timeout=30;')
    conn_str = 'mssql+pyodbc:///?odbc_connect=' + params
    engine = create_engine(conn_str)
    return engine
engine = get_engine_for_sql_server()


def get_connection_for_sql_server():
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';PORT=1433;DATABASE=' + database
        + ';UID=' + username + ';PWD=' + password)
    return connection


def get_df_from_sql_server(connection, sql_statement):
    cursor = connection.cursor()
    cursor.execute(sql_statement)
    return cursor


def add_table_to_sql_server(connection, sql_statement):
    success_flg = False
    try:
        cursor = connection.cursor()
        cursor.execute(sql_statement)
        connection.commit()
        success_flg = True
    except Exception as e:
        print(e)
    finally:
        connection.close()
    return success_flg


def insert_df_to_table(df, table_name, append_replace):
    success_flg = False
    try:
        engine = get_engine_for_sql_server()
        insert_statement = get_insert_statement(df)
        # df.convert_dtypes()
        df.to_sql(table_name, engine, if_exists=append_replace, index=False)
        #cursor = connection.cursor()
        # Insert Dataframe into SQL Server:
        #for index, row in df.iterrows():
        #    cursor.execute("INSERT INTO " + table_name + " (" + column_list + ") values(?,?,?)",
        #                   row.DepartmentID, row.Name, row.GroupName)
        #connection.commit()
        success_flg = True
    except Exception as e:
        print(e)
    return success_flg


@event.listens_for(engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
    if executemany:
        cursor.fast_executemany = True


def fast_load(df, table_name, append_replace):
    df.to_sql(table_name, engine, index=False, if_exists=append_replace, schema="dbo")


def bulk_insert_df_to_table(df, table_name, append_replace):
    success_flg = False
    connection = get_connection_for_sql_server()
    try:
        engine = get_engine_for_sql_server()
        insert_statement = get_insert_statement(df, table_name)
        cursor = connection.cursor()
        cursor.fast_executemany = True
        for row_count in range(0, df.shape[0]):
            chunk = df.iloc[row_count:row_count + 1, :].values.tolist()
            tuple_of_tuples = tuple(tuple(x) for x in chunk)
            cursor.executemany(
                insert_statement,
                # "insert into test" + " ([col_name1],   col_name2],[col_name3],[col_name4],[col_name5],[col_name6],[col_name7],[col_name8],[col_name9],[col_name10]) values   (?,?,?,?,?,?,?,?,?,?)",
                tuple_of_tuples)
        cursor.commit()
        # df.convert_dtypes()
        # df.to_sql(table_name, engine, if_exists=append_replace, index=False)
        #
        # Insert Dataframe into SQL Server:
        #for index, row in df.iterrows():
        #    cursor.execute("INSERT INTO " + table_name + " (" + column_list + ") values(?,?,?)",
        #                   row.DepartmentID, row.Name, row.GroupName)
        #connection.commit()
        success_flg = True
    except Exception as e:
        print(e)
    finally:
        connection.close()
    return success_flg


def get_insert_statement(df, table_nm):
    column_list = df.columns.values.tolist()
    comma_sep_list = ",".join(column_list)
    value_list = ""
    for x in column_list:
        value_list += "?,"
    value_list = value_list[:-1]
    insert_statement = 'INSERT INTO ' + table_nm + ' (' + comma_sep_list + ') VALUES (' + value_list + ")"
    return insert_statement