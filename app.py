# 1. import Flask / dependencies
import datetime as dt
from flask.globals import session

from werkzeug.exceptions import RequestHeaderFieldsTooLarge
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, json, jsonify

# -----------------------------------------------------------
# set up the database
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
#reflect tables
Base.prepare(engine, reflect=True) 
# create references 
Measurement = Base.classes.measurement
Station = Base.classes.station
#create a session link from python to our database
session = Session(engine)

# Create an app, being sure to pass __name__
app = Flask(__name__)

#import app

print("example __name__ = %s", __name__)

if __name__ == "__main__":
    print("example is being run directly.")
else:
    print("example is being imported")

# 3. Define what to do when a user goes to the index route
@app.route("/")
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

if __name__ == '__main__':
    app.run(debug=True)

@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)