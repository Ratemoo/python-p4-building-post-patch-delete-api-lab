#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries', methods=['GET'])
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(bakeries, 200)

@app.route('/bakeries/<int:id>', methods=['GET'])
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if bakery:
        bakery_serialized = bakery.to_dict()
        return make_response(bakery_serialized, 200)
    else:
        return make_response({'error': 'Bakery not found'}, 404)

@app.route('/baked_goods/by_price', methods=['GET'])
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [bg.to_dict() for bg in baked_goods_by_price]
    return make_response(baked_goods_by_price_serialized, 200)

@app.route('/baked_goods/most_expensive', methods=['GET'])
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    if most_expensive:
        most_expensive_serialized = most_expensive.to_dict()
        return make_response(most_expensive_serialized, 200)
    else:
        return make_response({'error': 'No baked goods found'}, 404)

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    new_baked_good = BakedGood(
        name=data.get('name'),
        price=float(data.get('price')),
        bakery_id=int(data.get('bakery_id'))  # Assuming this field exists in the form
    )
    db.session.add(new_baked_good)
    db.session.commit()

    return make_response(jsonify(new_baked_good.to_dict()), 201)  # 201 Created

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    data = request.form
    bakery = Bakery.query.get(id)
    
    if not bakery:
        return make_response({'error': 'Bakery not found'}, 404)
    
    if 'name' in data:
        bakery.name = data['name']
        db.session.commit()
        
    return make_response(jsonify(bakery.to_dict()), 200)

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)

    if not baked_good:
        return make_response({'error': 'Baked good not found'}, 404)

    db.session.delete(baked_good)
    db.session.commit()

    return make_response({'message': 'Baked good deleted successfully.'}, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
