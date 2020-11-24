import json
from flask import request, jsonify, g
from csaiweb.models import Login, Thread, Comments, Faculty, db
from csaiweb import app
import pandas as pd
import datetime

# Frontend Routes


@app.route('/', methods=["GET", "POST"])
def catch():
    return app.send_static_file('index.html')


@app.route('/about', methods=["GET", "POST"])
def catch_about():
    return app.send_static_file('index.html')


@app.route('/faculty', methods=["GET", "POST"])
def catch_faculty():
    return app.send_static_file('index.html')


@app.route('/annoucement', methods=["GET", "POST"])
def catch_announcement():
    return app.send_static_file('index.html')


@app.route('/opportunity', methods=["GET", "POST"])
def catch_opportunity():
    return app.send_static_file('index.html')


@app.route('/society', methods=["GET", "POST"])
def catch_society():
    return app.send_static_file('index.html')


@app.route('/forum', methods=["GET", "POST"])
def catch_forum():
    return app.send_static_file('index.html')


@app.route('/login', methods=["GET", "POST"])
def catch_login():
    return app.send_static_file('index.html')


@app.route('/signup', methods=["GET", "POST"])
def catch_signup():
    return app.send_static_file('index.html')


@app.route('/newthread', methods=["GET", "POST"])
def catch_newthread():
    return app.send_static_file('index.html')


@app.route('/thread/<id>', methods=["GET", "POST"])
def catch_thread(id):
    return app.send_static_file('index.html')


@app.route('/users/<username>', methods=["GET", "POST"])
def catch_users(username):
    return app.send_static_file('index.html')

# Backend Routes

# Route to return all faculty info


@app.route('/backend/faculty', methods=["GET"])
def faculty():
    users = Faculty.query.all()
    List = []
    Dict = {}

    for user in users:
        Dict = {
            'sno': user.sno,
            'name': user.name,
            'designation': user.designation,
            'qualification': user.qualification,
            'email': user.email,
            'number': user.number,
            'image': user.image
        }
        List.append(Dict)

    return json.dumps(List)

# Forum Route - Returns all Threads in database


@app.route('/backend/forum', methods=["GET"])
def forum():
    posts = Thread.query.all()
    List = []
    Dict = {}

    for post in posts:
        Dict = {
            'id': post.id,
            'title': post.title,
            'author': post.author,
            'karma': post.karma,
            'time_created': post.time_created
        }
        List.append(Dict)

    return json.dumps(List)

# Thread Backend Routes


@app.route('/backend/newthread', methods=["POST"])
def newthread():
    try:
        author = g.user
        content = request.get_json()
        title = content["title"]
        body = content["body"]
        time = datetime.datetime.now()
        upvoted = 0
        downvoted = 0
        karma = 0

        post = Thread(body=body, author=author, title=title, karma=karma,
                      upvoted=upvoted, downvoted=downvoted, time_created=time.strftime("%x"))

        db.session.add(post)
        db.session.commit()
        return 'New Thread Added', 200
    except:
        return 'Thread Not Added', 501


@app.route('/backend/editthread', methods=["GET", "PUT"])
def editthread():
    try:
        content = request.get_json()
        body = content["body"]
        sno = content["id"]
        upvoted = content["upvoted"]
        downvoted = content["downvoted"]
        karma = content["karma"]

        post = Thread.query.filter(Thread.id == sno).first
        post.body = body
        post.upvoted = upvoted
        post.downvoted = downvoted
        post.karma = karma
        db.session.commit()
        return 'Thread Updated!', 200
    except:
        return 'Thread Not Updated!', 501


@app.route('/backend/deletethread', methods=["GET", "DELETED", "POST"])
def deletethread():
    try:
        content = request.get_json()
        sno = content["id"]

        post = Thread.query.filter(Thread.id == sno).first
        db.session.delete(post)
        db.session.commit()
        return 'Thread Deleted!', 200
    except:
        return 'Thread Not Deleted!', 501


@app.route('/backend/thread/<id>', methods=["GET"])
def thread(id):

    row = Thread.query.get(id)
    List = []
    Dict = {
        'id': row.id,
        'body': row.body,
        'author': row.author,
        'title': row.title,
        'karma': row.karma,
        'upvoted': row.upvoted,
        'downvoted': row.downvoted,
        'time_created': row.time_created
    }
    List.append(Dict)

    return json.dumps(List)


# Comments Backend Routes
@app.route('/backend/newcomment', methods=["POST"])
def newcomment():
    try:
        author = g.user
        content = request.get_json()
        body = content["body"]
        thread_id = content["thread_id"]
        time = datetime.datetime.now()
        upvoted = 0
        downvoted = 0
        karma = 0

        post = Comments(body=body, author=author, thread_id=thread_id, karma=karma,
                        upvoted=upvoted, downvoted=downvoted, time_created=time.strftime("%x"))

        db.session.add(post)
        db.session.commit()
        return 'New Comment Added', 200
    except:
        return 'Comment Not Added', 501


@app.route('/backend/editcomment', methods=["GET", "PUT"])
def editcomment():
    try:
        content = request.get_json()
        body = content["body"]
        sno = content["id"]
        upvoted = content["upvoted"]
        downvoted = content["downvoted"]
        karma = content["karma"]

        post = Comments.query.filter(Comments.id == sno).first
        post.body = body
        post.upvoted = upvoted
        post.downvoted = downvoted
        post.karma = karma
        db.session.commit()
        return 'Comment Updated!', 200
    except:
        return 'Comment Not Updated!', 501


@app.route('/backend/deletecomment', methods=["GET", "DELETED", "POST"])
def deletecomment():
    try:
        content = request.get_json()
        sno = content["id"]

        post = Comments.query.filter(Comments.id == sno).first
        db.session.delete(post)
        db.session.commit()
        return 'Thread Deleted!', 200
    except:
        return 'Thread Not Deleted!', 501


@app.route('/backend/comments/<thread_id>', methods=["GET"])
def comments(thread_id):

    rows = Comments.query.filter(Comments.thread_id == thread_id).all()
    List = []
    Dict = {}

    for row in rows:
        Dict = {
            'id': row.id,
            'body': row.body,
            'author': row.author,
            'karma': row.karma,
            'thread_id': row.thread_id,
            'upvoted': row.upvoted,
            'downvoted': row.downvoted,
            'time_created': row.time_created
        }
        List.append(Dict)

    return json.dumps(List)

# User Info Display


@app.route('/backend/users/<username>', methods=["GET"])
def user(username):

    threads = Thread.query.filter(Thread.author == username).all()
    List = []
    Dict = {}

    for post in threads:
        Dict = {
            'type': "Thread",
            'id': post.id,
            'title': post.title,
            'author': post.author,
            'time_created': post.time_created
        }
        List.append(Dict)

    comments = Comments.query.filter(Comments.author == username).all()

    for row in comments:
        Dict = {
            'type': "Comments",
            'id': row.id,
            'body': row.body,
            'author': row.author,
            'thread_id': row.thread_id,
            'time_created': row.time_created
        }
        List.append(Dict)

    return json.dumps(List)