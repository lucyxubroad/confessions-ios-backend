import json
from db import db, Post, Comment, User
from flask import Flask, request

from math import sin, cos, sqrt, atan2, radians
import datetime
import users_dao

db_filename = "confessions3.db"
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

with app.app_context():
    db.create_all()
    

def extract_token(request):
  auth_header = request.headers.get('Authorization')
  if auth_header is None:
      return False, json.dumps({'error': 'Missing authorization header.'})

  # Header looks like "Authorization: Bearer <session token>"
  bearer_token = auth_header.replace('Bearer ', '').strip()
  if bearer_token is None or not bearer_token:
      return False, json.dumps({'error': 'Invalid authorization header.'})

  return True, bearer_token

def get_distance(long1, lat1, long2, lat2):
  R = 6373.0
  lat1 = radians(lat1)
  long1 = radians(long1)
  lat2 = radians(lat2)
  long2 = radians(long2)
  dlat = lat2 - lat1
  dlong = long2 - long1
  a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlong / 2)**2
  c = 2 * atan2(sqrt(a), sqrt(1 - a))
  distance = R * c
  return distance

def get_time_diff(time_beg):
  time_now = datetime.datetime.now()
  elapsedTime = time_now - time_beg
  time_difference_in_minutes = elapsedTime / datetime.timedelta(minutes=1)
  print(time_difference_in_minutes)
  return (time_difference_in_minutes < 1440)

@app.route('/')
def hello():
  return 'Hello World!'

@app.route('/api/posts/')
def get_posts():
  """Retrieves list of all posts."""
  posts = Post.query.all()
  res = {'success': True, 'data': [post.serialize() for post in posts]}
  return json.dumps(res), 200

@app.route('/api/posts/long=<string:long>&lat=<string:lat>/')
def get_post_by_location(long, lat):
  """Retrieves list of posts made in location vicinity."""
  long = float(long)
  lat = float(lat)
  posts = Post.query.all()
  response_body = []
  for post in posts:
    distance = get_distance(long, post.longitude, lat, post.latitude)
    time_expired = get_time_diff(post.time_created)
    print(time_expired)
    print(distance)
    if (distance < 5000 and time_expired):
      response_body.append(post.serialize())
  res = res = {'success': True, 'data': response_body}
  return json.dumps(res), 200

@app.route('/api/posts/', methods=['POST'])
def create_post():
  """Append new post to list."""
  post_body = json.loads(request.data)
  if 'username' in post_body and 'text' in post_body:
    post = Post (
      text = post_body.get('text'),
      username = post_body.get('username'),
      longitude = post_body.get('longitude'),
      latitude = post_body.get('latitude')
    )
    db.session.add(post)
    db.session.commit()
    return json.dumps({'success': True, 'data': post.serialize()}), 200
  return json.dumps({'success': False, 'error': 'Invalid POST body!'}), 404

@app.route('/api/post/<int:post_id>/')
def get_post(post_id):
  """Retrieve specific post in post list."""
  post = Post.query.filter_by(id=post_id).first() 
  if post is not None:
    return json.dumps({'success': True, 'data': post.serialize()}), 200
  return json.dumps({'success': False, 'error': 'Post not found!'}), 404


@app.route('/api/post/<int:post_id>/', methods=['POST'])
def edit_post(post_id):
  """Update specific post with new post"""
  post_body = json.loads(request.data)
  if 'text' not in post_body:
    return json.dumps({'success': False, 'error': 'Invalid POST body!'}), 404
  post = Post.query.filter_by(id=post_id).first()
  if post is not None:
    post.text = post_body.get('text', post.text)
    db.session.commit()
    return json.dumps({'success': True, 'data': post.serialize()}), 200
  return json.dumps({'success': False, 'error': 'Post not found!'}), 404

@app.route('/api/post/<int:post_id>/', methods=['DELETE'])
def delete_post(post_id):
  """Remove specific post in post list."""
  post = Post.query.filter_by(id=post_id).first() 
  if post is not None:
    db.session.delete(post)
    db.session.commit()
    return json.dumps({'success': True, 'data': post.serialize()}), 200
  return json.dumps({'success': False, 'error': 'Post not found!'}), 404 

@app.route('/api/post/<int:post_id>/comments/')
def get_comments(post_id):
  """Retrieve all comments for specific post."""
  post = Post.query.filter_by(id=post_id).first()
  if post is not None:
    comments = [comment.serialize() for comment in post.comments]
    return json.dumps({'success': True, 'data': comments}), 200
  return json.dumps({'success': False, 'error': 'Post not found!'}), 404

@app.route('/api/post/<int:post_id>/vote/', methods=['POST'])
def vote_post(post_id):
  """Vote on a post."""
  post_body = json.loads(request.data)
  post = Post.query.filter_by(id=post_id).first()
  if post is not None:
    if post_body['vote'] or 'vote' not in post_body:
      post.score = post.score + 1
    else:
      post.score = post.score - 1
    db.session.commit()
    return json.dumps({'success': True, 'data': post.serialize()}), 200
  return json.dumps({'success': False, 'error': 'Invalid post!'}), 404


@app.route('/api/post/<int:post_id>/comment/', methods=['POST'])
def comment_post(post_id):
  """Vote on a post."""
  post_body = json.loads(request.data)
  post = Post.query.filter_by(id=post_id).first()
  if post is not None:
    comment = Comment(
      text = post_body['text'],
      username = post_body['username'],
      post_id=post.id
    )
    post.comment_count = post.comment_count + 1
    post.comments.append(comment)
    db.session.add(comment)
    db.session.commit()
    return json.dumps({'success': True, 'data': post.serialize()}), 200
  return json.dumps({'success': False, 'error': 'Invalid post!'}), 404

@app.route('/register/', methods=['POST'])
def register_account():
    post_body = json.loads(request.data)
    email = post_body.get('email')
    password = post_body.get('password')

    if email is None or password is None:
        return json.dumps({'error': 'Invalid email or password'})

    created, user = users_dao.create_user(email, password)

    if not created:
        return json.dumps({'error': 'User already exists.'})

    return json.dumps({
        'session_token': user.session_token,
        'session_expiration': str(user.session_expiration),
        'update_token': user.update_token,
        'user_id': user.id,
        'photo_id': user.id%5
    })

@app.route('/login/', methods=['POST'])
def login():
    post_body = json.loads(request.data)
    email = post_body.get('email')
    password = post_body.get('password')

    if email is None or password is None:
        return json.dumps({'error': 'Invalid email or password'})

    success, user = users_dao.verify_credentials(email, password)

    if not success:
        return json.dumps({'error': 'Incorrect email or password.'})

    return json.dumps({
        'session_token': user.session_token,
        'session_expiration': str(user.session_expiration),
        'update_token': user.update_token,
        'user_id': user.id,
        'photo_id': user.id%5
    })

@app.route('/session/', methods=['POST'])
def update_session():
    success, update_token = extract_token(request)

    if not success:
        return update_token

    try:
        user = users_dao.renew_session(update_token)
    except: 
        return json.dumps({'error': 'Invalid update token.'})

    return json.dumps({
        'session_token': user.session_token,
        'session_expiration': str(user.session_expiration),
        'update_token': user.update_token,
        'user_id': user.id,
        'photo_id': user.id%5
    })

@app.route('/secret/', methods=['GET'])
def secret_message():
    success, session_token = extract_token(request)

    if not success:
        return session_token 

    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token):
        return json.dumps({'error': 'Invalid session token.'})

    return json.dumps({'message': 'You have successfully implemented sessions.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
