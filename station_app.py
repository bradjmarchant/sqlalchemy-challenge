import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# # reflect an existing database into a new model
Base = automap_base()
# # reflect the tables
Base.prepare(engine, reflect=True)

# # Save reference to the table
#Passenger = Base.classes.passenger
station = Base.classes.station
measurement = Base.classes.measurement


app=Flask(__name__)

@app.route("/")
def home():
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitations():
    session = Session(engine)

    # Query all passengers
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Perform a query to retrieve the data and precipitation scores
    past_year = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= query_date).all()

    session.close()

    # Convert list of tuples into normal list
    all_prcp = dict(past_year)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(station.station ).all()
    station_count = list(np.ravel(stations))
    session.close()
    return jsonify(station_count)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temps = session.query(measurement.tobs).\
    filter(measurement.station == 'USC00519281').\
    filter(measurement.date >= query_date).all()
    tobs = list(np.ravel(temps))
    session.close()
    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    start_temps = session.query(func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)).\
    filter(measurement.date == start).all()
    dates = list(np.ravel(start_temps))
    session.close()
    return jsonify(dates)

@app.route("/api/v1.0/<start>/<end>")
def date_range(start,end):
    session = Session(engine)
    temp_range = session.query(func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)).\
    filter(measurement.date >= start).filter(measurement.date <= end).all()
    temp_range = list(np.ravel(temp_range))
    session.close()
    return jsonify(temp_range)

if __name__=="__main__":
    app.run(debug=True)