#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get (self):
        plants=Plant.query.all()
        response_dict=[plant.to_dict()for plant in plants]

        response= make_response(response_dict,200)
        return response

    def post(self):
            data= request.get_json()
            new_plant= Plant(name=data['name'],image=data['image'],price=data['price'])

            db.session.add(new_plant)
            db.session.commit()

            return make_response(new_plant.to_dict(),200)

class PlantByID(Resource):
       def get (self,id):
            response_dict =  Plant.query.filter_by(id=id).first().to_dict()
            response= make_response(response_dict, 200)
            return response


class PlantByName(Resource):
       def get(self, name):
            response_dict = Plant.query.filter_by(name = name).first().to_dict()
            response = make_response(response_dict,200)
            return response
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')
api.add_resource(PlantByName, '/plants/name/<string:name>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
