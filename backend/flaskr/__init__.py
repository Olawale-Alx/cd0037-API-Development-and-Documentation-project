import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

TRIVIA_QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    """
    This function takes request and selected page as parameters and return number of questions based on the TRIVIA_QUESTIONS_PER_PAGE variable.
    """
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * TRIVIA_QUESTIONS_PER_PAGE
    end = start + TRIVIA_QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r'/*': {'origins': '*'}})


    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        """
        Sets allowed headers and methods for each CORS request
        """
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, DELETE, PATCH, POST, OPTIONS')

        return response


    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def all_categories():
        """
        ALL_CATEGORIES: /categories endpoint
        This endpoint sends all categories to the client. Sends a server error (500) if the server encountered an error
        """
        try:
            categories = Category.query.all()

            # Formats the category to send to frontend in an object format
            format_categories = {}
            for category in categories:
                format_categories[category.id] = category.type

            return jsonify({
                'success': True,
                'categories': format_categories,
                'total_categories': len(format_categories)
            })

        except:
            abort(500)



    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def questions():
        """
        This endpoint gets questions paginated by QUESTIONS_PER_PAGE and and sends the response to the front-end. Returns 404 error if resource cannot be found
        """
        questions = Question.query.order_by(Question.id).all()
        categories = Category.query.order_by(Category.id).all()
        total_questions = len(questions)

        current_questions = paginate_questions(request, questions)

        # Check whether length of current question is less than 1. If true, abort
        if len(current_questions) == 0:
            abort(404)
        
        # Formats the category to send to frontend in an object format
        format_categories = {}
        for category in categories:
            format_categories[Category.id] = category.type

        return jsonify({
            'success': True,
            'total_questions': total_questions,
            'questions': current_questions,
            'categories': 'categories'
        }), 200          


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """
        DELETE QUESTIONS: /questions/question_id endpoint
        This endpoint deletes question based on delete click from the client. Sends a client request error (422) if the request could not be processed
        """
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            # question = Question.query.filter(id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            questions = Question.query.order_by(Question.id).all()
            total_questions = len(Question.query.all())
            current_questions = paginate_questions(request, questions)

            return jsonify({
                'success': True,
                'deleted_id': question_id,
                'questions': current_questions,
                'total_questions': total_questions
            }), 200

        except:
            abort(422)


    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_new_question():
        """
        CREATE_NEW_QUESTION: /questions endpoint
        This endpoint creates new question from the client input. Sends a client request error (422) if the request could not be processed
        """
        question_body = request.get_json()

        # This adds data for new id lines into the database
        new_question = question_body.get('question', None)
        new_answer = question_body.get('answer', None)
        new_category = question_body.get('category', None)
        new_difficulty = question_body.get('difficulty', None)

        # Gets the question_search keyword
        question_search = question_body.get('search', None)

        if ((new_question == '') or (new_answer == '') or (new_category == '') or (new_difficulty == '')):
            
            abort(422)

        try:
            """
            @TODO:
            Create a POST endpoint to get questions based on a search term.
            It should return any questions for whom the search term
            is a substring of the question.

            TEST: Search by any phrase. The questions list will update to include
            only question that include that string within their question.
            Try using the word "title" to start.
            """
            # Check if the search was passed with an empty string. If true, abort
            if question_search == '':
                abort(422)
            
            # If false, search for the string in the database and return the search
            elif question_search:
                questions = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(question_search)))

                current_questions = paginate_questions(request, questions)

                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(current_questions)
                }), 200

            else:
                question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
                question.insert()

                questions = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, questions)

                return jsonify({
                    'success': True,
                    'message': 'new question was successfully added',
                    'created': question.id,
                    'questions': current_questions,
                    'total_questions': len(Question.query.all())
                })

        except:
            abort(422)


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def questions_by_category(category_id):
        """
        GET_QUESTIONS_BY_CATEGORY: /categories/category_id/questions endpoint
        This endpoint gets questions by categories. Sends a resource not found error (404) if the request could not be processed
        """
        category = Category.query.filter_by(id=id).one_or_none()

        if category is None:
            abort(404)

        questions = Question.query.filter(category.id == category_id).order_by(Category.id).all()

        current_question = paginate_questions(request, questions)

        return jsonify({
            'success': True,
            'questions': current_question,
            'total_questions': len(questions),
            'current_category': Question.query.filter(Question.category == category_id).all()
        }), 200


    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def start_quiz():
        """
        START_QUIZ: /quizzes endpoint
        This endpoint plays the trivia. Sends a bad request error (400) if the request could not be processed
        """
        data = request.get_json()
        previous_questions = data.get('previous_questions')
        categories = data.get('categories')

        if (previous_questions is None) or (categories is None):
            abort(400)

        if categories['id'] == 0:
            questions = Question.query.all()

        else:
            questions = Question.query.filter_by(category=categories['id']).all()

        def get_random():
            return questions[random.randint(0, len(questions)-1)]

        next_quiz_question = get_random()

        question_found = True

        while question_found:
            if next_quiz_question.id in previous_questions:
                next_quiz_question = get_random()
            
            else:
                question_found = False

        return jsonify({
            'success': True,
            'question': next_quiz_question.format()
        }), 200


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error_message': 'Request could not be processed due to internal server error. Try later'
        }), 500

    
    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            'success': False,
            'error_message': 'Resource not found. Check your request and try again'
        }), 404


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error_message': 'Unprocessable: Request could not be processed'
        }), 422


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error_message': 'bad request made by client'
        }), 400


    return app
