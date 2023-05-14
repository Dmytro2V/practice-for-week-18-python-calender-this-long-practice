"""Main routes
"""
import os
from datetime import datetime, timedelta
import psycopg2
import psycopg2.extras
from flask import Blueprint, render_template, redirect, url_for

from app.forms import AppointmentForm

# from flask import render_template

bp = Blueprint('/main', __name__, url_prefix='/')
CONNECTION_PARAMETERS = {
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASS"),
    "dbname": os.environ.get("DB_NAME"),
    "host": os.environ.get("DB_HOST"),
}


@bp.route("/", methods = ['GET'])
def main():
    '''Main route'''
    current_date_time = datetime.now() # has {year month day}
    year = current_date_time.year
    month = current_date_time.month
    day = current_date_time.day
    return redirect(url_for('.daily', year = year, month = month, day = day))

@bp.route("/<int:year>/<int:month>/<int:day>", methods = ['GET', 'POST'])
def daily(year, month, day):
    '''Copies main route but for day selected
    renders daily appoints... and what about form?
    '''
    form = AppointmentForm()
    if form.validate_on_submit(): # POST and valid
        # create a new record in the database
        with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
            with conn.cursor() as curs:
                q_select = """
                INSERT INTO appointments (
                    name, start_datetime, end_datetime, 
                    description, private
                    )
                VALUES (
                    %(name)s, %(start_datetime)s, %(end_datetime)s, 
                    %(description)s, %(private)s
                    )
                ;"""
                params = {
                    'name': form.name.data,
                    'start_datetime': datetime.combine(form.start_date.data, form.start_time.data),
                    'end_datetime': datetime.combine(form.end_date.data, form.end_time.data),
                    'description': form.description.data,
                    'private': form.private.data
                }

                curs.execute(q_select, params)
                return redirect('/')

    # Create a psycopg2 connection with the connection parameters
    print('Form is not submit or validated')
    with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
        print('Setting connection')
        # constuct from args:
        day = datetime(year, month, day) # pylint: disable = unused-variable
        next_day = day + timedelta(days = 1)

        # Create a cursor from the connection
        ### extras makes dictionary read instead of tuples
        with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as curs:
            # Execute "SELECT id, name, start_datetime, end_datetime
            q_select = """
                SELECT id, name, start_datetime, end_datetime
                FROM appointments
                WHERE start_datetime BETWEEN %(day)s AND %(next_day)s
                ORDER BY start_datetime
            ;"""
            params = {
                'day': day,
                'next_day': next_day
            }
            curs.execute(q_select, params)
            # Fetch all of the records
            rows = curs.fetchall()
            # for row in rows:
            #     print(row['id'])
            #     print("id: {}".format(row['id']))
            #     print("Last Name: {}".format(row['name']))
            #     print("Email: {}".format(row['start_datetime']))
    return render_template("main.html", rows=rows, form=form)
