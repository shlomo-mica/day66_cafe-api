from typing import Union, Any, Sequence
import dict
import flask

dict1 = dict
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


@app.route('/second_function', methods=['GET'])
def get_random_cafe():
    with app.app_context():
        response = db.session.execute(select(Cafe).where(Cafe.id == 5))
        response2 = db.session.execute(select(Cafe))
        result = db.session.execute(db.select(Cafe))

        all_cafes1 = result.scalars().all()
        serial_list = []
        for Row in all_cafes1:
            data = {'id': Row.id,
                    'name': Row.name,
                    'map': Row.map_url,
                    'img_url': Row.img_url,
                    'location': Row.location}
            serial_list.append(data)
        print(serial_list)
        # return (all_cafes1[20].location)
        return jsonify(cafe=serial_list)


@app.route("/")
def home():
    get_random_cafe()
    return render_template("index.html", get=get_random_cafe())


@app.route('/random', methods=["GET"])
def random_cafe():
    result = db.session.execute(db.select(Cafe))  # <class 'sqlalchemy.engine.result.ChunkedIteratorResult'>

    all_cafes_list = result.scalars().all()  # list

    rand_cafe = random.choice(all_cafes_list)

    return jsonify(cafe={
        # Omit the id from the response
        # "id": rand_cafe.id,
        "name": rand_cafe.name,
        "map_url": rand_cafe.map_url,
        "img_url": rand_cafe.img_url,
        "location": rand_cafe.location})

    # # Put some properties in a sub-category
    # "amenities": {
    #     "seats": rand_cafe.seats,
    #     "has_toilet": rand_cafe.has_toilet,
    #     "has_wifi": rand_cafe.has_wifi,
    #     "has_sockets": rand_cafe.has_sockets,
    #     "can_take_calls": rand_cafe.can_take_calls,
    #     "coffee_price": rand_cafe.coffee_price,
    # }


@app.route('/get_all_cafes', methods=['GET'])
def all_cafes():
    data = db.session.execute(db.select(Cafe).filter_by(name='Social - Copeland Road')).scalar_one()
    print(data.location)
    cafa_list_object = db.session.execute(db.select(Cafe).order_by(Cafe.id))
    result = Cafe.query.all()

    return jsonify([item.serialize() for item in result])

    # return jsonify(cafe_2={
    #     "name": all_cafeslist[item].name,
    #     "map_url": all_cafeslist[item].map_url,
    #     "img_url": all_cafeslist[item].img_url,
    #     "location": all_cafeslist[item].location})


# result = session.execute(
#     select(User).where(User.id == 5)

## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record



if __name__ == '__main__':
    app.run(debug=True)
