#!/usr/bin/python3
""" Starts a Flask web application """

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_HBNB():
    """ Displays 'Hello HBNB!' """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def HBNB():
    """ Displays 'HBNB' """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def C(text):
    """ Displays 'C' followed by the text passed """
    return "C {}".format(text.replace('_', ' '))


@app.route('/python', strict_slashes=False, defaults={'text': 'is cool'})
@app.route('/python/<text>', strict_slashes=False)
def p(text):
    """ Displays 'Python' followed by the text passed """
    return "Python {}".format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def n(n):
    """Display "'passed number' is a number"
       only if passed variable is an integer
    """
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def temp(n):
    """Displays a HTML page if passed variable n is an integer"""
    return render_template('5-number.html', n=n)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
