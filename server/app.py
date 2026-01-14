from flask import Flask, jsonify
from models import db, Earthquake

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/earthquakes/<int:id>")
def get_earthquake_by_id(id):
    quake = Earthquake.query.filter_by(id=id).first()

    if quake:
        return jsonify({
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        }), 200
    else:
        return jsonify({
            "message": f"Earthquake {id} not found."
        }), 404


@app.route("/earthquakes/magnitude/<float:magnitude>")
def get_earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(
        Earthquake.magnitude >= magnitude
    ).all()

    return jsonify({
        "count": len(quakes),
        "quakes": [
            {
                "id": quake.id,
                "location": quake.location,
                "magnitude": quake.magnitude,
                "year": quake.year
            }
            for quake in quakes
        ]
    }), 200
