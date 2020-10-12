import numpy as np
import pandas as pd

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

base = automap_base()
base.prepare(engine,reflect = True)

print(base.classes.keys())

measurements = base.classes.measurement
stations = base.classes.station

session = Session(engine)
conn = engine.connect()

app = Flask(__name__)

@app.route('/')
def home():
    return(
    f'/api/v1.0/precipitation <br>' 
    f'/api/v1.0/stations <br>'
    f'/api/v1.0/tobs <br>'
    f'/api/v1.0/start <br>'
    f'/api/v1.0/start/end <br>'
    )
@app.route('/api/v1.0/precipitation')
def prcp():

    year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    msrm_data = session.query(measurements.date, measurements.prcp).filter(measurements.date >= year).all()
    prcp_dict = {}
    for x in msrm_data:
        prcp_dict[x[0]]= x[1]
    print(prcp_dict)

    return jsonify(prcp_dict)

@app.route('/api/v1.0/stations')
def Station():
    stations_q=session.query(stations.station).all()
    return jsonify(stations_q)




if __name__ == '__main__':
    app.run()