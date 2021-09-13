#!/usr/bin/python3
""" Starts a web flask application to display
    a list of states and their cities
"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def list_states_cities():
    """ Display a HTML page that lists all states and their Ids in a
        sorted order and their corresponding cities and their Ids
    """
    return render_template('8-cities_by_states.html',
                           states=storage.all('State').values())


@app.teardown_appcontext
def teardown(self):
    """ Remove SQLAlchemy Session """
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
