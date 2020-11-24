import json
from flask import request, jsonify, g, make_response
from csaiweb.models import Login, db, encode_auth_token
from csaiweb import app
from csaiweb.middleware import login_required


@app.route('/backend/login', methods=["POST"])
def login():
    content = request.get_json()
    username = content["username"]
    password = content["password"]

    user = Login.query.filter(Login.username == username).first()

    if user is None:
        return 'ID does not exist', 501

    token = encode_auth_token(username)

    dict = {
        'token': token.decode()
    }

    return make_response(jsonify(dict))


@app.route('/ayurinfo/backend/login', methods=["GET"])
@login_required
def decode_password():
    try:
        username = g.user

        user = Login.query.filter(Login.username == username).first()

        List = []

        dict = {
            'username': user.username,
        }
        List.append(dict)

        return json.dumps(List)
    except:
        return 'server error', 500


@app.route('/backend/signup', methods=["POST"])
def signup():
    try:
        content = request.get_json()
        username = content["username"]
        password = content["password"]

        user = Login(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        token = encode_auth_token(username)

        dict = {
            'token': token.decode()
        }

        return make_response(jsonify(dict))
    except:
        return 'server error', 500
