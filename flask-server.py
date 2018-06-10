from flask import Flask, jsonify, Response, send_from_directory
from flask_restful import reqparse, abort, Api, Resource
from flask_pymongo import PyMongo

from bson.json_util import dumps, default
import os
from random import randint

app = Flask("test")
api = Api(app)
mongo = PyMongo(app)

# We'll use parser in put and post requests, so set it up here
# outside of the classes
parser = reqparse.RequestParser()
parser.add_argument('author')
parser.add_argument('content')

class QuoteList(Resource):
    def get(self):
        quotes = mongo.db.quotes.find().sort("index", -1).limit(10)
        resp = Response(dumps(quotes, default=default, indent=2),
                        mimetype='application/json')
        return resp

class Quote(Resource):
    def get(self, quote_id):
        quote_query = quote_id
        if quote_id == "random":
            quotes = mongo.db.quotes.find().sort("index", -1).limit(1)
            max_number = int(quotes[0]["index"])
            quote_query = randint(0, max_number)
        quotes = mongo.db.quotes.find_one({"index": int(quote_query)})
        resp = Response(dumps(quotes, default=default, indent=2),
                        mimetype='application/json')
        return resp

@app.route('/')
def hello_world():
    return 'Hello from Flask!'


@app.route('/demo/')
def serve_page():
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    STATIC_ROOT = os.path.join(APP_ROOT, "..", "..","..","static")
    return send_from_directory(STATIC_ROOT, "index.html")


api.add_resource(QuoteList, '/api/quotes')
api.add_resource(Quote, '/api/quotes/<quote_id>')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
