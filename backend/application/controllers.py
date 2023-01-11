from flask import Flask
from flask import render_template, request
from flask import current_app as app
from .models import  Tracker, Log

@app.route("/")
def trackers():
    trackers=Tracker.query.all()
    return render_template("trackers.html", trackers=trackers )