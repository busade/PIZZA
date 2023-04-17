import unittest
from flask import current_app, Flask
from .. import create_app
from ..config.config import config_dict
from ..utils import db




class UserTestCase(unittest.TestCase):
    def setUp(self) :
       self.app = create_app(config=config_dict['test'])
       self.appctx = self.app.app_context()
       self.appctx.push()
       self.client= self.app.test_client()

       db.create_all()

    def tearDown(self) :
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.client= None

    def test_user_reg(self):
        data = {
            'username':"why",
            'email': 'why@gmail.com',
            'password_hash': 'password'


        }

        response = self.client.post('/auth/signup', json= data)
        assert response.status_code == 201


    def test_login(self):
        data = {
            "email":"why@gmail.com",
            "password_hash":"password"
        }
        response = self.client.post('/auth/login', json = data)
        assert response.status_code == 400