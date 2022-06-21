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
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('student', 'student', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # This is a new question entry for testing
        self.new_question = {'question': 'Test question', 'answer': 'Test answer', 'category': 3, 'difficulty': 2}

        # Test to get questions by category
        self.quiz_request_data = {'previous_questions': [2, 4], 'quiz_category': {'type': 'Sports', 'id': 6}}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    """
    Notes on test

        # Asserts that categories is present in the return data
        self.assertTrue(data['categories'])
        
        # Asserts that categories length = 6 and is present in the return data
        self.assertEqual(data['total_categories'], 6)

        # Asserts that there is an error message in the return data
        self.assertEqual(data['error_message'])

        # Asserts that there is a total number of questions in the return data
        self.assertTrue(data['total_questions'])

        # Asserts that there are questions in the return data
        self.assertTrue(data['questions'])

        # Asserts that categories is present in the return data
        self.assertTrue(data['categories'])

    """
    def test_get_all_available_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(data['total_categories'], 6)

    
    def test_500_internal_server_error(self):
        response = self.client().get('/categories/500')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error_message'], 'Resource not found. Check your request and try again')


    def test_get_questions_with_paginations(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])


    def test_404_resource_questions_not_found(self):
        response = self.client().get('/questions?page=0')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error_message'], 'Resource not found. Check your request and try again')

    
    def test_delete_question_success(self):
        response = self.client().delete('/questions/17')
        data = json.loads(response.data)

        question = Question.query.filter(Question.id == 17).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(data['deleted_id'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(question, None)


    def test_422_request_not_processed(self):
        response = self.client().delete('/questions/0')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error_message'], 'Unprocessable: Request could not be processed')

    
    def test_post_new_questions(self):
        response = self.client().post('/questions', json=self.new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'], 'new question was successfully added')

    
    def test_422_eror_posting_new_question(self):
        response = self.client().post('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error_message'], 'bad request made by client')

    
    def test_get_questions_based_on_category(self):
        response = self.client().get('/categories/2/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])


    def test_404_invalid_category_id(self):
        response = self.client().get('/categories/1222/questins')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error_message'], 'resource not found')


    def test_start_quiz_questions(self):
        response = self.client().post('/quizzes', json=self.quiz_request_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['id'], 7)
        self.assertNotEqual(data['question']['id'], 3)
        self.assertEqual(data['question']['category'], 6)


    def test_400_bad_request_error(self):
        response = self.client().post('/quizzes', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error_message'], 'bad request made by client')
 

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
