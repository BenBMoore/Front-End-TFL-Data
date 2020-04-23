import functools
from pymongo import MongoClient
import ast
import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from tube_frontend.db import get_db, close_db

bp = Blueprint('tube-lines', __name__,)

@bp.route('/tube-lines', methods=['GET'])
def get_all_points():
    colours = {'northern': "#000000", "central": "#CC3333", "bakerloo": "#996633", "circle": "#FFCC00",
               "district": "#006633", "hammersmith-city": "#CC9999", "jubilee": "#868F98", "metropolitan": "#660066",
               "piccadilly": "#0019A8", "victoria": "#0099CC", "waterloo-city": "#66CCCC"}
    client = get_db()
    db = client["train-database"]
    features = []

    for row in db.line_collection.find():
        coords = row['lineStrings']
        line_colour = colours[row["line_id"]] if row["line_id"] in colours else "#CCCCC"
        for x in coords:
            x = ast.literal_eval(x)
            for y in x:
                features.append({
                    "type": "feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": y
                    },
                    "properties": {
                        "color": line_colour
                    }
                })
    close_db(client)
    body = json.dumps(features)
    header = json.loads('{ "type": "FeatureCollection","features":' + body + '}')
    return header, 200

@bp.route('/tube-stations', methods=['GET'])
def get_all_stations():
    colours = {'northern': "#000000", "central": "#CC3333", "bakerloo": "#996633", "circle": "#FFCC00",
               "district": "#006633", "hammersmith-city": "#CC9999", "jubilee": "#868F98", "metropolitan": "#660066",
               "piccadilly": "#0019A8", "victoria": "#0099CC", "waterloo-city": "#66CCCC"}
    features = []

    client = get_db()
    db = client["train-database"]

    for row in db.station_collection.find():
        features.append({
            "type": "feature",
            "geometry": {
                "type": "Point",
                "coordinates": row["coords"]
            },
            "properties": {
                "description": row["name"]
            }
        })
    body = json.dumps(features)
    close_db(client)
    header = json.loads('{ "type": "FeatureCollection","features":' + body + '}')
    return header, 200

@bp.route('/tube-trains', methods=['GET'])
def get_trains():
    colours = {'northern': "#000000", "central": "#CC3333", "bakerloo": "#996633", "circle": "#FFCC00",
               "district": "#006633", "hammersmith-city": "#CC9999", "jubilee": "#868F98", "metropolitan": "#660066",
               "piccadilly": "#0019A8", "victoria": "#0099CC", "waterloo-city": "#66CCCC"}
    features = []

    client = get_db()
    db = client["train-database"]

    for train in db.train_collection.find():
        features.append({
            "type": "feature",
            "geometry": {
                "type": "Point",
                "coordinates": train["currentLocation"]
            },
            "properties": {
                "title":train["id"],
                "description": train["currentLocationText"] + "<br>" + train["prevStation"] +"<br>" + train["nextStation"],
                "endLocation": train["nextStationCoords"],
                "timeToArrival":train["timeToStation"],
                "timeStamp":train["timestamp"],
                "route":train["route"],
            
            }
        })
    body = json.dumps(features)
    close_db(client)
    header = json.loads('{ "type": "FeatureCollection","features":' + body + '}')
    return header,200