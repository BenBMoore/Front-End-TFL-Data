from flask import Flask, render_template, jsonify
import json
from pymongo import MongoClient
import ast

app = Flask(__name__)


@app.route('/tube-lines', methods=['GET'])
def get_all_points():
    colours = {'northern': "#000000", "central": "#CC3333", "bakerloo": "#996633", "circle": "#FFCC00",
               "district": "#006633", "hammersmith-city": "#CC9999", "jubilee": "#868F98", "metropolitan": "#660066",
               "piccadilly": "#0019A8", "victoria": "#0099CC", "waterloo-city": "#66CCCC"}
    client = MongoClient('mongodb://localhost:27017/')
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
    body = json.dumps(features)
    header = json.loads('{ "type": "FeatureCollection","features":' + body + '}')
    return header


@app.route('/tube-stations', methods=['GET'])
def get_all_stations():
    colours = {'northern': "#000000", "central": "#CC3333", "bakerloo": "#996633", "circle": "#FFCC00",
               "district": "#006633", "hammersmith-city": "#CC9999", "jubilee": "#868F98", "metropolitan": "#660066",
               "piccadilly": "#0019A8", "victoria": "#0099CC", "waterloo-city": "#66CCCC"}
    features = []

    client = MongoClient('mongodb://localhost:27017/')
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
    header = json.loads('{ "type": "FeatureCollection","features":' + body + '}')
    return header

@app.route('/tube-trains', methods=['GET'])
def get_trains():
    colours = {'northern': "#000000", "central": "#CC3333", "bakerloo": "#996633", "circle": "#FFCC00",
               "district": "#006633", "hammersmith-city": "#CC9999", "jubilee": "#868F98", "metropolitan": "#660066",
               "piccadilly": "#0019A8", "victoria": "#0099CC", "waterloo-city": "#66CCCC"}
    features = []

    client = MongoClient('mongodb://localhost:27017/')
    db = client["train-database"]

    for train in db.train_collection.find():
        features.append({
            "type": "feature",
            "geometry": {
                "type": "Point",
                "coordinates": train["currentLocation"]
            },
            "properties": {
                "description": train["id"] + "<br>" + train["currentLocationText"] + "<br>" + train["prevStation"] +"<br>" + train["nextStation"],
            }
        })
    body = json.dumps(features)
    header = json.loads('{ "type": "FeatureCollection","features":' + body + '}')
    return header

@app.route('/')
def main():
    return render_template('main.html')


app.run(debug=True)
