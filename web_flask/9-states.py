#!/usr/bin/python3
""" Starts a web flask application to display
    a list of states and their cities
"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def list_states():
    """ Display a HTML page that lists all states and their Ids in a
        sorted order
    """
    return render_template('9-states.html',
                           states=storage.all('State').values(), id=None)


@app.route('/states/<id>', strict_slashes=False)
def list_states_cities(id=None):
    """ Display a HTML page that lists all sta Ids in a
        sorted order and their corresponding cities and their Ids
    """
    states = storage.all('State')
    key = 'State.{}'.format(id)
    if key in states:
        states = states[key]
    else:
        states = None

    return render_template('9-states.html', states=states, id=id)


@app.teardown_appcontext
def teardown(self):
    """ Remove SQLAlchemy Session """
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
