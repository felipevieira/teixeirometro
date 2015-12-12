#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
app = Flask(__name__)

def list_teams():
    return ['A', 'B', 'C']

@app.route("/")
def hello():
    return render_template('index.html', teams=list_teams())

@app.route("/<team>/")
def team(team):
    return render_template('team.html', name=team)

if __name__ == "__main__":
    app.run()
