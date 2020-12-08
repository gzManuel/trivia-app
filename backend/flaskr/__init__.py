import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                        'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                        'GET,PATCH,POST,DELETE,OPTIONS')
    return response   


  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()
    list_categories = {category.id: category.type for category in categories}
    if len(list_categories) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': list_categories
    })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  def paginate_questions(request, selection):
    # Function to paginate just 10 questions
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    # Using list comprehension.
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions

  @app.route('/questions')
  def get_questions():
    questions = Question.query.all()
    categories = Category.query.all()
    # Using dictionary comprehension.

    list_categories = {category.id: category.type.lower() for category
    in categories}
    list_questions = paginate_questions(request, questions)
    if len(list_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': list_questions,
      'total_questions': len(questions),
      'categories': list_categories,
      'current_category': None
    })
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id): 
    question = Question.query.filter_by(id=id).one_or_none()
    if question is None:
        abort(404)
    question.delete()
    return jsonify({
      'success': True,
      'deleted': id
    })

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def add_question():
    try:
      question = request.json.get('question')
      answer = request.json.get('answer')
      category = request.json.get('category')
      difficulty = request.json.get('difficulty')

      question = Question(
        question=question,
        answer=answer,
        category=category,
        difficulty=difficulty
      )
      question.insert()

      return jsonify({
        'success': True,
        'created': question.id
      })
    except:
      abort(422)
      
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    