import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, db, Movie, Actor

PRODUCER_TOKEN = None
ASSISTANT_TOKEN = None
DIRECTOR_TOKEN = None

class MainTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.getenv('TEST_DATABASE_URL')
        setup_db(self.app)


    def tearDown(self):
        """Executed after reach test"""
        pass


    """
    One test for success behavior of each endpoint
    One test for error behavior of each endpoint
    """


    # MOVIES
    def test_home_page(self):
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_movie(self):
        new_movie = {
            'title': 'Call Me by Your Name',
            'release_date': '2017-10-20'
        }
        headers = {
            'Authorization': "Bearer " + PRODUCER_TOKEN
        }
        res = self.client().post('/movies', json=new_movie, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_missing_post_movie_info(self):
        new_movie = {
            'title': '',
            'release_date': '2017-01-01'
        }
        auth = {
            'Authorization': "Bearer " + PRODUCER_TOKEN
        }
        res = self.client().post('/movies', json=new_movie, headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)


    def test_patch_movie(self):
        edit_movie = {
            'title': '',
            'release_date': '2020-11-01'
        }
        auth = {
            'Authorization': "Bearer " + DIRECTOR_TOKEN
        }
        res = self.client().patch('/movies/1', json=edit_movie,
                           headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_404_patch_movie_not_found(self):
        edit_movie = {
            'title': 'testing',
            'release_date': '2020-11-01'
        }
        auth = {
            'Authorization': "Bearer " + DIRECTOR_TOKEN
        }
        res = self.client().patch('/movies/100', json=edit_movie, headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_movies(self):
        auth = {
            'Authorization': "Bearer " + ASSISTANT_TOKEN
        }
        res = self.client().get('/movies', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_401_unauth_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertTrue(data['description'])

    def test_delete_movie(self):
        auth = {
            'Authorization': "Bearer " + PRODUCER_TOKEN
        }
        res = self.client().delete('/movies/1', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 1)
    
    def test_404_delete_movie_not_found(self):
        auth = {
            'Authorization': "Bearer " + PRODUCER_TOKEN
        }
        res = self.client().delete('/movies/100', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # Actors
    def test_post_acotr(self):
        new_actor = {
            'name': 'Timothée Chalamet',
            'age': 24,
            'gender': 'M',
            'movie_id': 1
        }
        auth = {
            'Authorizaton': "Bearer " + DIRECTOR_TOKEN
        }
        res = self.client().post('/actors', json=new_actor, headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_missing_post_actor_info(self):
        new_actor = {
            'name': 'Timothée Chalamet',
            'age': '',
            'gender': 'M',
            'movie_id': 1
        }
        auth = {
            'Authorization': "Bearer " + DIRECTOR_TOKEN
        }
        res = self.client().post('/actors', json=new_actor, headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_patch_actor(self):
        edit_actor = {
            'name': '',
            'age': 88,
            'gender': '',
            'movie_id': ''
        }
        auth = {
            'Authorization': "Bearer " + DIRECTOR_TOKEN
        }
        res = self.client().patch('/actors/1', json=edit_actor,
                           headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_404_patch_actor_not_found(self):
        edit_actor = {
            'name': '',
            'age': 88,
            'gender': '',
            'movie_id': ''
        }
        auth = {
            'Authorization': "Bearer " + DIRECTOR_TOKEN
        }
        res = self.client().patch('/actors/1000', json=edit_actor, headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_actors(self):
        auth = {
            'Authorization': "Bearer " + ASSISTANT_TOKEN
        }
        res = self.client().get('/actors', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_401_unauth_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertTrue(data['description'])

    def test_delete_actor(self):
        auth = {
            'Authorization': "Bearer " + DIRECTOR_TOKEN
        }
        res = self.client().delete('/actors/1', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 1)
    
    def test_404_delete_actor_not_found(self):
        auth = {
            'Authorization': "Bearer " + DIRECTOR_TOKEN
        }
        res = self.client().delete('/actors/1000', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # AUTH Test Cases
    def test_401_invalid_header_view_movie(self):
        auth = {
            'Authorization': "TOKEN " + ASSISTANT_TOKEN
        }
        res = self.client().get('/actors', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'invalid_header')
        self.assertTrue(data['description'])

    def test_401_invalid_token_view_actor(self):
        auth = {
            'Authorization': "Bearer" + 'asdfghjkl'
        }
        res = self.client().get('/actors', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertTrue(data['description'])

    def test_401_unauth_add_actor(self):
        new_actor = {
            'name': 'Linda Chen',
            'age': 24,
            'gender': 'F',
            'movie_id': 1
        }
        auth = {
            'Authorizaton': "Bearer " + ASSISTANT_TOKEN
        }
        res = self.client().post('/actors', json=new_actor, headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_401_unauth_modify_movie(self):
        edit_movie = {
            'title': '',
            'release_date': '2020-11-11'
        }
        auth = {
            'Authorization': "Bearer " + ASSISTANT_TOKEN
        }
        res = self.client().patch('/movies/1', json=edit_movie,
                           headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_401_unauth_delete_movie(self):
        auth = {
            'Authorization': "Bearer " + DIRECTOR_TOKEN
        }
        res = self.client().delete('/movies/1', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_401_unauth_add_movie(self):
        new_movie = {
            'title': 'To test',
            'release_date': '2017-10-20'
        }
        headers = {
            'Authorization': "Bearer " + DIRECTOR_TOKEN
        }
        res = self.client().post('/movies', json=new_movie, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)