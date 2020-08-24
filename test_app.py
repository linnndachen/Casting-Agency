import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from .database.models import setup_db, Movie, Actor

