from typing import Union, Any, Sequence

import flask
from flask import Flask, jsonify, render_template, request, json
from flask_sqlalchemy import SQLAlchemy
import random

from sqlalchemy import select, Row, RowMapping

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,

            'map_url': self.map_url,
            'img_url': self.img_url,
            'location': self.location,
            'seats': self.seats,
            'has_toilet': self.has_toilet,
            'has_wifi': self.has_wifi
        }


# MODEL


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/random', methods=["GET"])
def random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)

    return jsonify(cafe={
        # Omit the id from the response
        # "id": random_cafe.id,
        "name": random_cafe.name,
        "map_url": random_cafe.map_url,
        "img_url": random_cafe.img_url,
        "location": random_cafe.location})

    # # Put some properties in a sub-category
    # "amenities": {
    #     "seats": random_cafe.seats,
    #     "has_toilet": random_cafe.has_toilet,
    #     "has_wifi": random_cafe.has_wifi,
    #     "has_sockets": random_cafe.has_sockets,
    #     "can_take_calls": random_cafe.can_take_calls,
    #     "coffee_price": random_cafe.coffee_price,
    # }


@app.route('/get_all_cafes', methods=['GET'])
def all_cafes():
    result = Cafe.query.all()

    return jsonify([item.serialize() for item in result])

    # return jsonify(cafe_2={
    #     "name": all_cafeslist[item].name,
    #     "map_url": all_cafeslist[item].map_url,
    #     "img_url": all_cafeslist[item].img_url,
    #     "location": all_cafeslist[item].location})


# result = session.execute(
#     select(User).where(User.id == 5)
def get_random_cafe():
    with app.app_context():
        response = db.session.execute(select(Cafe).where(Cafe.id == 5))
        response2 = db.session.execute(select(Cafe))
        result = db.session.execute(db.select(Cafe))
        all_cafes1 = result.scalars().all()
        random_cafe = random.choice(all_cafes1)
    return response


## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
