import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import setup_db, Movie, Actor


class MainTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)


    def tearDown(self):
        """Executed after reach test"""
        pass


    """
    One test for success behavior of each endpoint
    One test for error behavior of each endpoint
    """
    #MOVIES
    def test_add_movie(self):
        pass


    def test_edit_movie(self):
        pass


    def test_get_movies(self):
        pass


    def test_delete_movie(self):
        pass