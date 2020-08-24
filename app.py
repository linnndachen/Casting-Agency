import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import exc

from database.models import setup_db, Movie, Actor
from auth.auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={"/": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, PUT, POST, DELETE, OPTIONS')
    return response

  #Home
  @app.route('/')
  def index():
    return jsonify({
    'message': 'Welcome to Casting Agency'
  })

  #Movie endpoints
  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies(payload):
    try:
      movies = Movie.query.all()
      return jsonify({
      'success': True,
      'movies': [movie.format() for movie in movies]
    }), 200
    except Exception:
      abort (500)

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def add_movie(payload):
    try:
      data = request.get_json()
      movie = Movie(
        title=data['title'],
        release_date=data['release_date']
      )
      movie.insert()

      return jsonify({
        'success': True,
        'movie': movie.format()
      }), 200

    except Exception:
      abort(422)

  @app.route('/movies/<int:id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(payload, id):
    try:
      new_info = request.get_json()
      movie = Movie.query.filter(Movie.id == id).one_or_none()
      if movie:
        movie.title = (new_info['title'] if new_info['title']
                      else movie.title)
        movie.release_date = (new_info['release_date'] if new_info['release_date']
                      else movie.release_date)

        movie.update()
      else:
        abort(404)
      return jsonify({
        'success': True,
        'movies': movie.format()
    }), 200
    except Exception:
      abort(500)

  @app.route('/movies/<int:id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload, id):
    try:
      movie = Movie.query.filter(Actor.id == id).one_or_none()
      if movie:
        movie.delete()
        return jsonify({
          'success': True,
          'delete': id
        }), 200
      else:
        abort(400)
    except Exception:
      abort(500)

  #Actor endpoints
  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors(payload):
    try:
      actors = Actor.query.all()
      return jsonify({
      'success': True,
      'movies': [actor.format() for actor in actors]
    }), 200
    except Exception:
      abort (500)


  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def add_actor(payload):
    try:
      data = request.get_json()
      actor = Actor(
        name=data['name'],
        age=data['age'],
        gender=data['gender']
      )
      actor.insert()

      return jsonify({
        'success': True,
        'movie': actor.format()
      }), 200

    except Exception:
      abort(422)


  @app.route('/actors/<int:id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(payload, id):
    try:
      new_info = request.get_json()
      actor = Actor.query.filter(Actor.id == id).one_or_none()
      if actor:
        actor.name = (new_info['name'] if new_info['name']
                      else Actor.name)
        actor.age = (new_info['age'] if new_info['age']
                      else actor.age)
        actor.gender = (new_info['gender'] if new_info['gender']
                      else actor.gender)

        actor.update()
      else:
        abort(404)
      return jsonify({
        'success': True,
        'movies': actor.format()
    }), 200
    except Exception:
      abort(500)


  @app.route('/actors/<int:id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, id):
    try:
      actor = Actor.query.filter(Actor.id == id).one_or_none()
      if actor:
        actor.delete()
        return jsonify({
          'success': True,
          'delete': id
        }), 200
      else:
        abort(400)
    except Exception:
      abort(500)

  #Error Handling
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found."
      }), 404


  @app.errorhandler(500)
  def internal_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "Sorry, there's a problem on our end."
      }), 500

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422, 
      'message': 'unprocessable. Check your input.'
    }), 422

  return app




APP = create_app()


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)