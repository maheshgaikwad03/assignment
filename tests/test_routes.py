import unittest
from app import app, db
from app.models import User, Recipe

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] =  'mysql://root:root@localhost/logindb'
        self.app = app.test_client()
        db.create_all()
        self.create_user()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_user(self):
        user = User(username='testuser', email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()

    def login(self):
        self.app.post(url_for('login'), data=dict(
            email='test@example.com',
            password='password'
        ), follow_redirects=True)

    def test_create_recipe(self):
        self.login()
        response = self.app.post(url_for('new_recipe'), data=dict(
            title='Test Recipe',
            description='Test Description',
            ingredients='Test Ingredients',
            instructions='Test Instructions'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your recipe has been created', response.data)
