#!/usr/bin/python3
""" Starts a web flask application to display list of states """

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def list_states():
    """ Display a HTML page that lists all states and their Ids in a
        sorted order
    """
    return render_template('7-states_list.html',
                           states=storage.all('State').values())


@app.teardown_appcontext
def teardown(self):
    """ Remove SQLAlchemy Session """
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
