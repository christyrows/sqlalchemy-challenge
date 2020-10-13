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
year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

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

@app.route('/api/v1.0/tobs')
def tobs():
    highest_year = session.query(measurements.tobs).filter(measurements.station == 'USC00519281').filter(measurements.date >= year).all()
    return jsonify(highest_year)




@app.route('/api/v1.0/<start>')
def just_start():
    avg_temp = session.query(func.min(measurements.tobs),func.max(measurements.tobs), func.avg(measurements.tobs)).filter(measurements.date > year).first()
    return jsonify(avg_temp)



@app.route('/api/v1.0/<start>/<end>')
def start_end():
    avg_temp_inclusive = session.query(func.min(measurements.tobs),func.max(measurements.tobs), func.avg(measurements.tobs)).filter(measurements.date >= year).first()
    return jsonify(avg_temp_inclusive)


if __name__ == '__main__':
    app.run()