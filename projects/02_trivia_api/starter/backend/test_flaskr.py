import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgres://{}/{}".format(
            'postgres:root@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # Test for Getting Questions with pagination

    def test_get_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'])

    def test_404_get_questions(self):
        res = self.client().get('/questions?page=200')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Test for Search Questions

    def test_search_questions(self):
        res = self.client().post('/questions', json={'searchTerm': 'title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    # Test for Delete Question

    def test_delete_question(self):
        res = self.client().delete('/questions/65')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_delete_question(self):
        res = self.client().delete('/questions/300')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # Test for Getting Questions by Categories

    def test_get_questions_by_categories(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_404_get_questions_by_categories(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Test for Adding Question

    def test_add_question(self):
        res = self.client().post('/questions',
                                 json={'question': 'Smart', 'answer': 'tv', 'difficulty': 1, 'category': 2})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_add_question(self):
        res = self.client().post('/questions',
                                 json={'question': 'Smart', 'answer': 'tv', 'difficulty': 1, 'category': 9})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # Test for getting random questions to play the quiz
    def test_get_questions_to_play_quiz(self):
        res = self.client().post(
            '/quizzes', json={'previous_questions': [], 'quiz_category': {'type': 'Science', 'id': '1'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])

    def test_404_get_questions_to_play_quiz(self):
        res = self.client().post(
            '/quizzes', json={'previous_questions': [], 'quiz_category': {'type': 'Science', 'id': '9'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    # Test for adding users

    def test_add_users(self):
        res = self.client().post('/users', json={'name': 'Lukas'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['name'])
        # self.assertTrue(data['id'])

    # Test for updating user score

    def test_update_user_score(self):
        res = self.client().patch('/users', json={'id': 1, 'score': 4})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['id'])
        self.assertEqual(data['success'], True)

    def test_422_update_user_score(self):
        res = self.client().patch('/user', json={'id': 7, 'score': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # Test for Adding Categories

    def test_add_categories(self):
        res = self.client().post('/categories', json={'type': 'Books'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['type'])
        self.assertEqual(data['success'], True)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
