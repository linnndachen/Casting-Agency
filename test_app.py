import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, db


PRODUCER_TOKEN = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im8wZUlrUzMyNzVFM3pBQnRKcUsxZiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctcHJvamVjdC51cy5hdXRoMC5jb20vIiwic3ViIjoiSnlkM0NyZWtLQmxZWjlpQmMwN0YxZEtZalk2UlhxTVZAY2xpZW50cyIsImF1ZCI6Imh0dHA6Ly9sb2NhbGhvc3Q6ODA4MCIsImlhdCI6MTU5ODc0NzU5NiwiZXhwIjoxNTk4ODMzOTk2LCJhenAiOiJKeWQzQ3Jla0tCbFlaOWlCYzA3RjFkS1lqWTZSWHFNViIsInNjb3BlIjoiZ2V0Om1vdmllcyBnZXQ6YWN0b3JzIHBvc3Q6bW92aWVzIHBvc3Q6YWN0b3JzIHBhdGNoOmFjdG9ycyBwYXRjaDptb3ZpZXMgZGVsZXRlOmFjdG9ycyBkZWxldGU6bW92aWVzIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOlsiZ2V0Om1vdmllcyIsImdldDphY3RvcnMiLCJwb3N0Om1vdmllcyIsInBvc3Q6YWN0b3JzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiXX0.P0LokP_8FLbKbMUvjB0lUQqc_ECuXVAyXKHA0OJBj-y3olS8QLoDXzwKOV96acjA3RnV4E_XU_YGP8uadrhHT09BFYLeupqKuzRPky_hHfqtHNDFDVCvZdNZZx2Fmj_5mXx702f0HTJ2uYW3Hfsz5POx5YGBJPO_N4jpG7-ISyxLe3iUfBDBWczB2iqLelcmGIUSTEsvS2InYDbYl0pd5tdlhsb-32HF7etKcepAHosERRS0G0N4r4GhW1b2Ohk8VpHlb3PmMGTIQ3cIasPnmx-xdkXKr0N9OFIapDdPkxp2p7SnTfnVPBuX_CL5i6ES-VzGsbqot1x2qKRKiUQcZQ')
ASSISTANT_TOKEN = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im8wZUlrUzMyNzVFM3pBQnRKcUsxZiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctcHJvamVjdC51cy5hdXRoMC5jb20vIiwic3ViIjoiSnlkM0NyZWtLQmxZWjlpQmMwN0YxZEtZalk2UlhxTVZAY2xpZW50cyIsImF1ZCI6Imh0dHA6Ly9sb2NhbGhvc3Q6ODA4MCIsImlhdCI6MTU5ODc0Nzc1NywiZXhwIjoxNTk4ODM0MTU3LCJhenAiOiJKeWQzQ3Jla0tCbFlaOWlCYzA3RjFkS1lqWTZSWHFNViIsInNjb3BlIjoiZ2V0Om1vdmllcyBnZXQ6YWN0b3JzIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOlsiZ2V0Om1vdmllcyIsImdldDphY3RvcnMiXX0.jB8h02q-AhbWgMPkagMgjYZouSzn-aLaYkJ3OCaDzkLY48HnkmN6et0fsH6F_6QL8pCVCuMXDCjZQnVJwCqxbufhgtJkEgcf18IImVkvrj-dcMCmmVeljaNvERiSilJGo4Wg82eicyqOX1bnfiTGwZVHZbEMwDoy36fitd3G0ok5p9R__SMfz0Q0DtFoUBGp-ENVGKWC-MyGQOU6oUnoyOAKlfAujKvY8MNIPnU3AXDtIirJe4CgO-vQNhe1_Uy58hD2c8f7tu_JxbVXUFu_ACezWzrNpDrlIffB08PqLJYNEnzaS3T4EruSX9mmBRPz-m6Jwo89ejhF2lFciJ1ocQ')
DIRECTOR_TOKEN = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im8wZUlrUzMyNzVFM3pBQnRKcUsxZiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctcHJvamVjdC51cy5hdXRoMC5jb20vIiwic3ViIjoiSnlkM0NyZWtLQmxZWjlpQmMwN0YxZEtZalk2UlhxTVZAY2xpZW50cyIsImF1ZCI6Imh0dHA6Ly9sb2NhbGhvc3Q6ODA4MCIsImlhdCI6MTU5ODc0NzY5NCwiZXhwIjoxNTk4ODM0MDk0LCJhenAiOiJKeWQzQ3Jla0tCbFlaOWlCYzA3RjFkS1lqWTZSWHFNViIsInNjb3BlIjoiZ2V0Om1vdmllcyBnZXQ6YWN0b3JzIHBvc3Q6YWN0b3JzIHBhdGNoOmFjdG9ycyBwYXRjaDptb3ZpZXMgZGVsZXRlOmFjdG9ycyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbImdldDptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwicG9zdDphY3RvcnMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIl19.MqZGO9bDIvLEwDHxEcAE6vbF06go-1NHOD0Vk7TLezvl8ljB2P_HYrnSGFbfQxWNGXRAWOJjByAALcTZrdh4F89HeLBM6H7Q9u0zGRWhA17Yot8ggOh6UUzOBKzmPLNsjDHsYWQ4_ePc7pgpo4M5t9vZlBBz1B_OyEK3_ucpAMPliPLgmrq0ynw2sRA3om2SGtylILc2KTyjz-v-qVKJs-rvajv9lajIHtniVAUhGXFy7InJE7Vw4ttLUxv1uNQVksdCjSV-qYgQq7VHh4jDyDtq9HJvHJM1uByu8xHE_I11zYyXHhmWVf2nua_cAy1Yb6lbTHVSVQJf1VX9ikd4nQ')


class MainTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

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

        self.assertEqual(res.status_code, 200)

    def test_post_movie(self):
        new_movie = {
            'title': 'Call Me by Your Name',
            'release_date': '2017-10-20'
        }
        headers = {
            'Content-Type': 'application/json',
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
        res = self.client().patch('/movies/3', json=edit_movie,
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
        res = self.client().get('/movies', headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')

    def test_delete_movie(self):
        auth = {
            'Authorization': "Bearer " + PRODUCER_TOKEN
        }
        res = self.client().delete('/movies/2', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 2)

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
    def test_post_actor(self):
        new_actor = {
            'name': 'Timothée Chalamet',
            'age': 24,
            'gender': 'M',
            'movie_id': 6
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer " + DIRECTOR_TOKEN
        }
        res = self.client().post('/actors', json=new_actor, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_missing_post_actor_info(self):
        new_actor = {
            'name': 'TEST',
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
        res = self.client().patch('/actors/3', json=edit_actor,
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
        res = self.client().patch('/actors/1000', json=edit_actor,
                                  headers=auth)
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
        res = self.client().get('/actors', headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')

    def test_delete_actor(self):
        auth = {
            'Authorization': "Bearer " + DIRECTOR_TOKEN
        }
        res = self.client().delete('/actors/2', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 2)

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

    def test_401_invalid_token_view_actor(self):
        auth = {
            'Authorization': "Bearer" + 'asdfghjkl'
        }
        res = self.client().get('/actors', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'invalid_header')

    def test_403_unauth_add_actor(self):
        new_actor = {
            'name': 'Linda Chen',
            'age': 24,
            'gender': 'F',
            'movie_id': 1
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(ASSISTANT_TOKEN)
        }
        res = self.client().post('/actors', json=new_actor, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'],
                         'You are not allowed to access this resource')

    def test_403_unauth_modify_movie(self):
        edit_movie = {
            'title': '',
            'release_date': '2020-11-11'
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(ASSISTANT_TOKEN)
        }
        res = self.client().patch('/movies/4', json=edit_movie,
                                  headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'],
                         'You are not allowed to access this resource')

    def test_403_unauth_delete_movie(self):
        auth = {
            'Authorization': "Bearer {}".format(DIRECTOR_TOKEN)
            }
        res = self.client().delete('/movies/6', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'],
                         'You are not allowed to access this resource')

    def test_403_unauth_add_movie(self):
        new_movie = {
            'title': 'To test',
            'release_date': '2017-10-20'
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(DIRECTOR_TOKEN)
            }
        res = self.client().post('/movies', json=new_movie, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'],
                         'You are not allowed to access this resource')
