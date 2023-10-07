from typing import Union, Any, Sequence

import flask

from flask import Flask, jsonify, render_template, request, json
from flask_sqlalchemy import SQLAlchemy
import random

from sqlalchemy import select, Row, RowMapping, update

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
def add_shop():
    # new_caffe = dict(name1="AROMA", location="haifa")
    # exists22 = db.session.query(db.where(Cafe.id == 21))
    # response = db.session.execute(select(Cafe).where(Cafe.id == 5))
    exists = bool(db.session.query(Cafe).filter_by(name='Ark_CAFE').first())
    print(exists)
    if exists == True:
        try:
            add_coffee = Cafe(name="CAFFEINE",
                              map_url="TTTT",
                              img_url="bbbb",
                              location="haifa",
                              seats=22,
                              has_toilet=True,
                              has_wifi=True,
                              has_sockets=True,
                              can_take_calls=True,
                              coffee_price=56)
            db.session.add(add_coffee)
            db.session.commit()
        except:
            print("ALREADY EXIST")


with app.app_context():
    db.create_all()


@app.route('/update-price/<cafe_id>', methods=['GET'])
def price_change(cafe_id):
    coffeeid = request.args.get("id_number")
    new_price = request.args.get("updated_price")
    # update_price = db.session.query(Cafe).filter_by(name=coffeeid).first()# NO POSSIBLE TONENTER ID
    # update_price.coffee_price = new_price
    # db.session.commit()
    user_update_price = db.session.execute((db.select(Cafe).where(Cafe.id == coffeeid))).scalar()
    user_update_price.coffee_price = new_price
    db.session.commit()

    # update_name = db.session.query(Cafe).filter_by(name='aroma').first()
    # update_name.name = 'new_aroma'

    # cafe_to_delete = Cafe.query.filter_by(id=22).first()
    # # Check if the user exists
    # if cafe_to_delete:
    #     # Delete the user
    #     db.session.delete(cafe_to_delete)
    #     db.session.commit()

    # stmt = (db.update(Cafe).where(Cafe.id == coffeeid).values(coffee_price=new_price))
    # data_patch = db.session.execute(Cafe).all()
    return jsonify(changes={'coffee_id': coffeeid, 'new_value': new_price})


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
                    'location': Row.location,
                    'coffee_price': Row.coffee_price
                    }
            serial_list.append(data)
        # print(serial_list)
        # return (all_cafes1[20].location)
        return jsonify(cafe=serial_list)


@app.route("/")
def home():
    get_random_cafe()
    add_shop()
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
    #     "seats": Row.seats,
    #     "has_toilet": Row.has_toilet,
    #     "has_wifi": Row.has_wifi,
    #     "has_sockets": Row.has_sockets,
    #     "can_take_calls": Row.can_take_calls,
    #     "coffee_price": Row.coffee_price,
    # }


@app.route('/search/<area>', methods=['GET'])
def search_cafe_locations(area):
    # TODO make query search coffies in the same area
    shops = db.session.execute(select(Cafe).where(Cafe.location == f'{area}'))
    coffee_shops = shops.scalars().all()
    l22 = []
    # print(coffee_shops)
    for Row in coffee_shops:
        data = ({'name': Row.name,
                 "seats": Row.seats,
                 "has_toilet": Row.has_toilet,
                 "has_wifi": Row.has_wifi,
                 "has_sockets": Row.has_sockets,
                 "can_take_calls": Row.can_take_calls,
                 "coffee_price": Row.coffee_price,
                 }
        )
        l22.append(data)

    return jsonify(locations=l22)


# return jsonify(cafe={"name": shops.name})

# Omit the id from the response
# "id": rand_cafe.id,


# result = session.execute(
#     select(User).where(User.id == 5)

@app.route('/get_all_cafes', methods=['GET'])
def all_cafes():
    data = db.session.execute(db.select(Cafe).filter_by(name='Social - Copeland Road')).scalar_one()
    # print(data.location)
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
@app.route("/search")
def get_cafe_at_location():
    query_location = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    # Note, this may get more than one cafe per location
    all_cafes = result.scalars().all()
    if all_cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404


if __name__ == '__main__':
    app.run(debug=True)
from sqlalchemy import update
