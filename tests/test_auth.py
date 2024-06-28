import unittest
from app import app, db
from app.models import User
from flask import url_for

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] =  'mysql://root:root@localhost/logindb'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register(self):
        response = self.app.post(url_for('register'), data=dict(
            username='testuser',
            email='test@example.com',
            password='password',
            confirm_password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your account has been created', response.data)

    def test_login(self):
        user = User(username='testuser', email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()
        response = self.app.post(url_for('login'), data=dict(
            email='test@example.com',
            password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login Unsuccessful', response.data)
