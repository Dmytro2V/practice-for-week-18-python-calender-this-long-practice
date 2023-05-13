"""Main routes
"""
import os
import psycopg2
import psycopg2.extras
from flask import Blueprint, render_template, redirect

from app.forms import AppointmentForm

# from flask import render_template

bp = Blueprint('/main', __name__, url_prefix='/')
CONNECTION_PARAMETERS = {
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASS"),
    "dbname": os.environ.get("DB_NAME"),
    "host": os.environ.get("DB_HOST"),
}


@bp.route("/", methods = ['GET', 'POST'])
def main():
    '''Main route'''
    form = AppointmentForm()
    if form.validate_on_submit(): # POST and valid
        # create a new record in the database
        with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
            with conn.cursor() as curs:
                q_select = ("""
                INSERT INTO appointments (
                    name, start_time, end_time
                    )
                VALUES (%(name)s, %(start_datetime)s,
                    %(end_datetime)s
                    )"""
               )

                curs.execute(q_select,
                    {'name': form.name,
                    'start_datetime': form.start_time,
                    'end_datetime': form.end_time
                    })


        return redirect('/')

    # Create a psycopg2 connection with the connection parameters
    with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
        print(conn.get_dsn_parameters())
        # Create a cursor from the connection
        ### extras makes dictionary read instead of tuples
        with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as curs:
            # Execute "SELECT id, name, start_datetime, end_datetime
            q_select = """
                SELECT id, name, start_datetime, end_datetime
                FROM appointments
                ORDER BY start_datetime;"""
            curs.execute(q_select)
            # Fetch all of the records
            rows = curs.fetchall()
            # for row in rows:
            #     print(row['id'])
            #     print("id: {}".format(row['id']))
            #     print("Last Name: {}".format(row['name']))
            #     print("Email: {}".format(row['start_datetime']))
    return render_template("main.html", rows=rows, form=form)
