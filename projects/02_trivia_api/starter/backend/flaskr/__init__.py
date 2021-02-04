import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, User

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  def get_categories():
      categories = Category.query.all()
      if len(categories) == 0:
            abort(404)

      else:
          all_categories = {}
          for category in categories:
              all_categories[category.id] = category.type
          return all_categories


  @app.route('/categories', methods=['GET', 'POST'])
  def all_categories():
      # GET CATEGORIES
      if request.method == 'GET':
          return jsonify({'categories': get_categories()})
      else:
          # ADD CATEGORIES
          try:
              data = request.get_json()
              category_type = data.get('type')
              if not category_type:
                  abort(404)
              category = Category(type=category_type)
              category.insert()
              return jsonify({
                  'success': True,
                  'type': category_type,
                  'categories': get_categories()
              })
          except:
              abort(422)

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
  @app.route('/questions', methods=['GET', 'POST'])
  def get_questions():
        if request.method == 'GET':
              # GET ALL QUESTIONS
              selection = Question.query.order_by(Question.id).all()
              questions = paginate_questions(request, selection)

              if len(questions) == 0:
                    abort(404)
              else:
                    return jsonify({
                        'success': True,
                        'questions': questions,
                        'total_questions': len(selection),
                        'categories': get_categories(),
                        'current_category': 'All'
                    })
        else:
              data = request.get_json()
              searchTerm = data.get('searchTerm')
              if searchTerm:
                  # SEARCH QUESTIONS
                    try:
                      category_selection = Question.query.join(Category, Question.category == Category.id).filter(
                          Question.question.ilike('%' + searchTerm + '%')).all()

                      selection = Question.query.filter(
                          Question.question.ilike('%' + searchTerm + '%')).all()

                      if len(selection) == 0:
                            abort(404)
                            return jsonify({
                                'success': False,
                                'message': 'resource not found'
                            })
                      else:
                            questions = paginate_questions(request, selection)
                            current_category = {}
                            current_category[category_selection[0]
                                            .category] = category_selection[0].category_question.type

                            return jsonify({
                                'success': True,
                                'questions': questions,
                                'total_questions': len(questions),
                                'current_category': current_category
                            })
                    except:
                      abort(404)
                      return jsonify({
                        'success': False,
                        'message': 'resource not found'
                      })
              else:
                    # INSERT QUESTION
                    try:
                      qst = data.get('question')
                      answer = data.get('answer')
                      category = data.get('category')
                      difficulty = data.get('difficulty')
                      if not qst or not answer:
                            abort(422)
                      else:
                            question = Question(question=qst, answer=answer,
                                              category=category, difficulty=difficulty)
                            question.insert()

                            return jsonify({
                                'success': True
                            })
                    except:
                      abort(422)
                      return jsonify({
                          'success': False
                      })

  # DELETE QUESTION
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
        try:
          question = Question.query.filter(
              Question.id == question_id).one_or_none()
          
          if question is None:
                abort(422)
                return jsonify({
                    'success': False
                })
          else:
                question.delete()

                return jsonify({
                  'success': True
                })
        except:
          abort(422)
          return jsonify({
              'success': True
          })
  # GET QUESTIONS BASED ON CATEGORIES
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_categories(category_id):
        selection = Question.query.filter(Question.category==category_id).all()
        questions = paginate_questions(request, selection)

        if len(questions) == 0:
            abort(404)
        else:
            current_category = {}
            current_category[category_id] = get_categories()[category_id]
            return jsonify({
                'success': True,
                'questions': questions,
                'total_questions': len(selection),
                'current_category': current_category
            })


  # GET QUESTIONS TO PLAY QUIZ
  @app.route('/quizzes', methods=['POST'])
  def get_quiz_question():
        data = request.get_json()
        previous_questions = data.get('previous_questions')
        quiz_category = data.get('quiz_category')

        selection = Question.query.filter(
            Question.category == quiz_category['id']).all() if quiz_category['id'] != 0 else Question.query.all()

        if len(selection) != 0:
            current_questions = [question.format() for question in selection]

            filtered_questions = [
                qst for qst in current_questions if qst['id'] not in previous_questions]

            random_choice = random.choice(filtered_questions) if len(
                filtered_questions) != 0 else False
            # print(random.choice(filtered_questions))

            return jsonify({
                'question': random_choice,
                'success': True
            })
        else:
              abort(404)

  # Add Users/Update Users and Users Scores
  @app.route('/users', methods=['GET', 'POST', 'PATCH']) 
  def add_user():
      data = request.get_json()
      
      if request.method == 'POST':
          # Insert Users
          name = data.get('name')
          if not name:
              abort(404)
          user = User(name=name, score=0)
          try:
              user.insert()
              return jsonify({
                  'success': True,
                  'name': name
              })
          except:
              abort(422)  

      elif request.method == 'PATCH':
          # Update User Scores
          id = data.get('id')
          score = data.get('score')
          user = User.query.get(id)
          if user and score:
              try:
                  user.score = score
                  user.update()
                  return jsonify({
                      'success': True,
                      'id': id,
                      'score': score
                  })
              except:
                  abort(422)
          else:
              abort(404) 

      else:
          users = User.query.all()
          if len(users) == 0:
              abort(404)
          else:
              all_users = [user.format() for user in users]
              return jsonify({
                  'success': True,
                  'users': all_users
              })


          

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

  @app.errorhandler(405)
  def not_found(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405

  @app.errorhandler(422)
  def not_found(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessed request"
    }), 422
  
  return app

    
