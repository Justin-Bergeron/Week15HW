# import necessary libraries
from sqlalchemy import func
import datetime as dt
import numpy as np
import pandas as pd

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine




#################################################
# Flask Setup
#################################################
from flask import Flask, jsonify, render_template
app = Flask(__name__)

#################################################
# Database Setup
#################################################
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/belly_button_biodiversity.sqlite"

base = automap_base()
#reflect the tables
Base.prepare(engine, reflect = True)
session = Session(engine)




db = SQLAlchemy(app)


class BB(db.Model):
    __tablename__ = 'BB'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    title = db.Column(db.String)
    classification = db.Column(db.String)
    timestamp = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __repr__(self):
        return '<BigFoot %r>' % (self.name)


# Create database classes
@app.before_first_request
def setup():
    # Recreate database each time for demo
    # db.drop_all()
    db.create_all()

#################################################
# Flask Routes
#################################################


# Query the database and send the jsonified results
@app.route("/data")
def data():
    sel = [func.strftime("%Y", Bigfoot.timestamp), func.count(Bigfoot.timestamp)]
    results = db.session.query(*sel).\
        group_by(func.strftime("%Y", Bigfoot.timestamp)).all()
    df = pd.DataFrame(results, columns=['months', 'sightings'])
    return jsonify(df.to_dict(orient="records"))


# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
