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
        self.client = self.app.test_client()
        self.database_name = "trivia_test"
        self.database_path = "postgres://manuel:1234@localhost:5432/{}".format( self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        self.new_question = {
            'question':'What is the highest-grossing film of all time without taking inflation into account?',
            'answer': 'Avengers: Endgame',
            'category':5,
            'difficulty':3
        }
        self.new_question_error={
            'question':'What is the highest-grossing film of all time without taking inflation into account?',
            'answer': 'Avengers: Endgame',
            'category':'Entertaiment',
            'difficulty':'Medium'
        }
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_questions(self):
        res = self.client.get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
    
    def test_get_categories(self):
        res = self.client.get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['categories'])

    # This method is skiped because there's no other way to success than deleting all the categories.
    # Deleting all Categories generates erros to others methods.
    @unittest.skip
    def test_404_get_categories(self):
        # Category.deleteAll()
        
        res = self.client.get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')
    
    def test_404_request_beyond_valid_page(self):
        res = self.client.get('/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')

    def test_delete_question(self):
        question_id=23
        res = self.client.delete('/questions/'+str(question_id))
        data = json.loads(res.data)

        question = Question.query.filter(Question.id==question_id).one_or_none()
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['deleted'],question_id)
        self.assertEqual(question,None)

    def test_404_delete_question(self):
        question_id=1000
        res = self.client.delete('/questions/'+str(question_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')
 
    def test_add_question(self):
        res = self.client.post('/questions', json = self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        question = Question.query.filter(Question.id==data['created']).one_or_none()
        
        self.assertEqual(data['success'],True)
        self.assertTrue(question)

    def test_422_add_question(self):
        res = self.client.post('/questions', json = self.new_question_error)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'unprocessable')

    def test_search_question(self):
        res = self.client.post('/questions/search', json={'searchTerm':'What'})
        data = json.loads(res.data) 

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertNotEqual(data['total_questions'],0)
    
    def test_404_search_question(self):
        res = self.client.post('/questions/search', json={'searchTerm':'I never be found'})
        data = json.loads(res.data) 

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')

    def test_get_by_category(self):
        res = self.client.get('/categories/1/questions')
        data = json.loads(res.data) 
        
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True) 
        self.assertNotEqual(data['total_questions'],0)
        self.assertTrue(data['questions'])
        self.assertTrue(data['current_category'])
    
    def test_404_get_by_category_not_found_category(self):
        res = self.client.get('/categories/100/questions')
        data = json.loads(res.data) 

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')
    
    def test_404_get_by_category_not_found_questions(self):
        res = self.client.get('/categories/7/questions')
        data = json.loads(res.data) 

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')

    def test_quizzes(self):
        id = 4
        parameters = {'previous_questions':[25],'quiz_category':{'id':id}}
        res = self.client.post('/quizzes', json=parameters)
        data = json.loads(res.data) 

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['question'])
        self.assertEqual(data['category'].get('id'),id)

    def test_finish_quizzes(self):
        id = 4
        parameters = {'previous_questions':[25],'quiz_category':{'id':id}}
        res = self.client.post('/quizzes',json=parameters)
        data = json.loads(res.data) 

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['question'])
        self.assertEqual(data['category'].get('id'),id)
   
    def test_422_quizzes(self):
        parameters = {'previous_questions':4,'quiz_category':{'id':'id'}}
        res = self.client.post('/quizzes',json=parameters)
        data = json.loads(res.data) 

        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()