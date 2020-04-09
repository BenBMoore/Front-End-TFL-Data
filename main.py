from flask import Flask, render_template, jsonify
import sqlite3
import ast

app = Flask(__name__)


@app.route('/geojson-features', methods=['GET'])
def get_all_points():
    colours = {'northern': "#FFFFFF", "central": "#CC3333", "bakerloo": "#996633", "circle": "#FFCC00",
               "district": "#006633", "hammersmith-city": "#CC9999", "jubilee": "#868F98", "metropolitan": "#660066",
               "piccadilly": "#0019A8", "victoria": "0099CC", "waterloo-city": "66CCCC"}
    conn = sqlite3.connect('C:\\Users\\bluer\\Documents\\Dev\\tfl-open-data\\example.db')
    c = conn.cursor()
    features = []
    for row in c.execute('SELECT id, line_coords FROM lines'):
        coords = ast.literal_eval(row[1])
        print(colours[row[0]])
        line_colour = colours[row[0]] if row[0] in colours else "#CCCCC"
        for x in coords:
            x = ast.literal_eval(x)
            for y in x:
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": y
                    },
                    "properties": {
                        "color": line_colour
                    }
                })

    return jsonify(features)


@app.route('/')
def main():
    return render_template('main.html')


app.run(debug=True)
