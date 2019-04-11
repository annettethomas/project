import sqlite3
import datetime
from flask import Flask, render_template, g

PATH = 'db/sqlite/bird.sqlite'

app = Flask(__name__)

def open_connection():
    connection = getattr(g, '_connection', None)
    if connection == None:
        connection = g._connection = sqlite3.connect(PATH)
    connection.row_factory = sqlite3.Row
    return connection

def execute_sql(sql, values=(), commit=False, single=False):
    connection = open_connection()
    cursor = connection.execute(sql, values)
    if commit == True:
        results = connection.commit()
    else:
        results = cursor.fetchone() if single else cursor.fetchall()

    cursor.close()
    return results

@app.teardown_appcontext
def close_connection(exception):
    connection = getattr(g, '_connection', None)
    if connection is not None:
        connection.close()

@app.route('/')

@app.route('/index')
def welcome():
    return render_template('index.html')

@app.route('/birdwatch')
def flights():
    flights = execute_sql('SELECT * FROM flights')
    return render_template('birdwatch.html', flights=flights)


@app.route('/Comics')
def comics():
    comics = execute_sql('SELECT * FROM comics')
    return render_template('comics.html', comics=comics)


@app.route('/Fantasy')
def fantasy():
    fantasys = execute_sql('SELECT * FROM fantasys')
    return render_template('fantasy.html', fantasys=fantasys)


if __name__ == '__main__':
    app.run(debug=True)
