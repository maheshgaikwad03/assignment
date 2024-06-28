import unittest
from app import db,app
from app.models import User, Recipe

class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] =  'mysql://root:root@localhost/logindb'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_creation(self):
        user = User(username='testuser', email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(User.query.count(), 1)

    def test_recipe_creation(self):
        user = User(username='testuser', email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()
        recipe = Recipe(title='Test Recipe', description='Test Description', ingredients='Test Ingredients',
                        instructions='Test Instructions', author=user)
        db.session.add(recipe)
        db.session.commit()
        self.assertEqual(Recipe.query.count(), 1)
