import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # Create and configure the app
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

    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        list_categories = {
            category.id: category.type for category in categories}
        if len(list_categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': list_categories
        })

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

    @app.route('/questions/search', methods=['POST'])
    def search_question():

        search_term = request.json.get('searchTerm')
        search = "%{}%".format(search_term)

        # To search all the questions with the search_term without case
        # sensitive
        questions = Question.query.filter(
            Question.question.ilike(search)).all()

        if len(questions) == 0:
            abort(404)
        format_questions = [question.format() for question in questions]
        print(format_questions)

        return jsonify({
            'success': True,
            'questions': format_questions,
            'total_questions': len(format_questions),
            'current_category': None
        })

    @app.route('/categories/<int:id>/questions')
    def get_questions_by_categories(id):
        category = Category.query.filter_by(id=id).one_or_none()
        if category is None:
            abort(404)
        questions = Question.query.filter_by(category=category.id).all()

        if len(questions) == 0:
            abort(404)
        format_questions = [question.format() for question in questions]

        return jsonify({
            'success': True,
            'questions': format_questions,
            'total_questions': len(questions),
            'current_category': category.format()
        })

    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        try:
            quiz_category = request.json.get('quiz_category')
            previous_questions = request.json.get('previous_questions')

            # If the quiz_category is 0 that means that plays with
            # all categories.
            if quiz_category['id'] != 0:
                # Getting questions of a specific category.
                questions = Question.query.filter_by(
                    category=quiz_category['id']).all()
            else:
                # Getting questions of all categories.
                questions = Question.query.all()
            # It uses the function nextQuestion() to get randomly the next
            # question.
            next_question = nextQuestion(previous_questions, questions)
            return jsonify({
                'success': True,
                'question': next_question,
                'category': quiz_category
            })
        except:
            abort(422)

    def nextQuestion(previous_questions_id, questions):

        new_questions = questions.copy()
        for x in range(len(questions)):
            # Check if there is no previous questions quizzed, and if is None,
            # break the loop
            if previous_questions_id is None:
                break
            # Removes a question that has been asked in the quizz
            for y in range(len(previous_questions_id)):
                if previous_questions_id[y] == questions[x].id:
                    new_questions.remove(questions[x])
        if len(new_questions) == 0:
            # When it returns None means that there're not more questions.
            return None
        else:
            # Return a random question between all the leftover questions.
            i = random.randint(0, len(new_questions)-1)
            return new_questions[i].format()

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    return app
