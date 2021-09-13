#!/usr/bin/python3
""" Starts a web flask application to display list of states and amenities """

from flask import Flask, render_template
from models import storage


app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def states_cities_amenities():
    """ Display a HTML page that lists all states and their Ids in a
        sorted order, their corresponding cities and a list of amenities
    """
    return render_template('10-hbnb_filters.html',
                           states=storage.all('State').values(),
                           amenities=storage.all('Amenity').values)


@app.teardown_appcontext
def teardown(self):
    """ Remove SQLAlchemy Session """
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
