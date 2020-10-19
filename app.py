import bson.json_util as json
from bson import ObjectId
from flask import Flask, request, Response
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_pyfile('config.py')
mongo = PyMongo(app)


def bson_response(d, status=200):
    d = json.dumps(d)
    return Response(d, status, headers={'Content-Type': 'application/json'})


@app.route('/todos', methods=['GET'])
def get_all_todos():
    return bson_response({
        'todos': list(mongo.db.todos.find({}))
    })


@app.route('/todos', methods=['POST'])
def put_todo():
    text = request.get_json(force=True).get('text')
    if text is None:
        return Response({'message': 'Invalid body'}, 422)
    inserted_id = mongo.db.todos.insert_one({
        'text': text,
        'completed': False
    }).inserted_id
    return bson_response({
        'id': inserted_id
    }, 201)


@app.route('/todos/<oid>', methods=['PATCH'])
def update_todo(oid):
    if not ObjectId.is_valid(oid):
        return Response({'message': 'Invalid ObjectId'}, 400)
    oid = ObjectId(oid)
    record = mongo.db.todos.find_one({'_id': oid})
    if record is None:
        return Response({'message': 'TODO not found'}, 404)

    data = request.get_json(force=True)
    text = data.get('text')
    completed = data.get('completed')
    upd = {}
    if text is not None:
        upd['text'] = text

    if completed is not None:
        upd['completed'] = completed

    if len(upd) != 0:
        mongo.db.todos.update_one({'_id': oid}, upd)

    return {'message': 'Success'}


@app.route('/todos/<oid>', methods=['DELETE'])
def delete_todo(oid):
    if not ObjectId.is_valid(oid):
        return Response({'message': 'Invalid ObjectId'}, 400)
    oid = ObjectId(oid)
    mongo.db.todos.delete_one({'_id': oid})
    return {'message': 'Deleted successfully'}


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)
