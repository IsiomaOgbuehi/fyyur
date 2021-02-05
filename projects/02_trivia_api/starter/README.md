# Trivia Game of Udacity

## Full Stack Trivia Game

This project is a practice trivia game for Udacity students. Individuals are able to: add questions specifying category and difficulty level,  delete questions, search questions, sort questions, and play the game. Scores are presented at the end of each game played. It serves as a practice module for a fullstack nanodegree with Udacity.

All backend code follows [PEP8 style guidelines.](https://www.python.org/dev/peps/pep-0008/)

As part of the completion requirements, API Endpoints have been developed to handle the following:

1) Display questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions with a requirement that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 
 

## Getting Started

Developers using this project should already have Python3, pip and node installed on their local machines.

### Backend

From the backend folder run pip install requirements.txt. All required packages are included in the requirements file.

In the `backend` folder path, run the following commands for DB Migration:

```bash
flask db init
flask db migrate
flask db upgrade
```

To run the application run the following commands:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the __init__.py file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation.](https://flask.palletsprojects.com/en/1.0.x/tutorial/factory/)

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration.


### Frontend

From the frontend folder, run the following commands to start the client:

```bash
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on `http://localhost:3000/`. 

### Tests

In order to run tests navigate to the backend folder and run the following commands:

```bash
dropdb trivia
createdb trivia
psql trivia < trivia.psql
python test_flaskr.py
```

## API Reference

### Getting Started

* Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
* Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
```

The API will return three error types when requests fail:

* 405: Method Not Allowed
* 404: Resource Not Found
* 422: Not Processable

### Endpoints

### GET /categories
* General
<<<<<<< HEAD
    * Returns all categories
    * [URI:-] (http://127.0.0.1:5000/categories)
    * Test: `curl -X GET http://127.0.0.1:5000/categories`
* Response:
=======
    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
    - Request Arguments: None
    - Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
* Sample: `curl -X GET http://127.0.0.1:5000/categories`
>>>>>>> ce0c1c80925c1e586e2884d82cb606be9f42ead0

```
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```

### GET /questions?page={page_number}
* General
<<<<<<< HEAD
    * Get questions with pagination
    * [URI:-] (http://127.0.0.1:5000/questions?page=1)
    * Test `curl -X GET http://127.0.0.1:5000/questions?page=1`
* Response:
=======
    - Get questions with pagination
    - Returns list of questions by pagination of 10, success, total_questions, categories, current_category.
* Sample: `curl -X GET http://127.0.0.1:5000/questions?page=1`
>>>>>>> ce0c1c80925c1e586e2884d82cb606be9f42ead0

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "All", 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 26
}
```

### POST /questions

* General
<<<<<<< HEAD
    * Search for questions with a search term
    * [URI:-] (http://127.0.0.1:5000/questions)
    * Test `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "lake"}'`
* Response: 
=======
    - Search for questions with a search term
    - Returns current_category, success, questions, total_questions
* Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "lake"}'`
>>>>>>> ce0c1c80925c1e586e2884d82cb606be9f42ead0

```
{
  "current_category": {
    "3": "Geography"
  }, 
  "questions": [
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

### DELETE /questions/{question_id}

* General
<<<<<<< HEAD
    * Delete questions with question id. Returns success if deleted.
    * [URI:-] (http://127.0.0.1:5000/questions/20)
    * Test `curl -X DELETE  http://127.0.0.1:5000/questions/20`
* Response:
=======
    - Delete questions with question id. Returns success if deleted.
* Sample: `curl -X DELETE  http://127.0.0.1:5000/questions/20`
>>>>>>> ce0c1c80925c1e586e2884d82cb606be9f42ead0

```
{
  "success": true
}
```

### GET /categories/1/questions

* General
<<<<<<< HEAD
    * Get Questions by category
    * [URI:-] (http://127.0.0.1:5000/categories/1/questions)
    * Test `curl -X GET  http://127.0.0.1:5000/categories/1/questions`
* Response:
=======
    - Get Questions by category
    - Returns current_category, success, questions, total_questions
* Sample: `curl -X GET  http://127.0.0.1:5000/categories/1/questions`
>>>>>>> ce0c1c80925c1e586e2884d82cb606be9f42ead0

```
{
  "current_category": {
    "1": "Science"
  }, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "creation", 
      "category": 1, 
      "difficulty": 3, 
      "id": 131, 
      "question": "Wonders"
    }, 
    {
      "answer": "tv", 
      "category": 1, 
      "difficulty": 1, 
      "id": 25, 
      "question": "Smart"
    }, 
    {
      "answer": "body", 
      "category": 1, 
      "difficulty": 3, 
      "id": 28, 
      "question": "Human machinery"
    }, 
    {
      "answer": "", 
      "category": 1, 
      "difficulty": 2, 
      "id": 134, 
      "question": ""
    }, 
    {
      "answer": "timed", 
      "category": 1, 
      "difficulty": 2, 
      "id": 135, 
      "question": "Players"
    }
  ], 
  "success": true, 
  "total_questions": 8
}
```

### POST /questions

* General
<<<<<<< HEAD
    * ADD Question
    * [URI:-] (http://127.0.0.1:5000/questions)
    * Test `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "Human Machinery", "answer": "Body", "difficulty": 3, "category": 1}'`
* Response:
=======
    - ADD Question with json body containing: question, answer, difficulty, category
    - Returns success as True if successful
* Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "Human Machinery", "answer": "Body", "difficulty": 3, "category": 1}'`
>>>>>>> ce0c1c80925c1e586e2884d82cb606be9f42ead0

```
{
  "success": true
}
```

### POST /quizzes

* General
<<<<<<< HEAD
    * Get random questions to play the quiz
    * [URI:-] (http://127.0.0.1:5000/quizzes)
    * Test `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [], "quiz_category": {"type": "Science", "id": "1"}}'`
* Response:
=======
    - Get random questions to play the quiz
    - Sends a json body which includes: a list of previous_questions, a dictionary of quiz_category
    - Returns success, question object containing; question, answer, category, difficutly, id
* Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [], "quiz_category": {"type": "Science", "id": "1"}}'`
>>>>>>> ce0c1c80925c1e586e2884d82cb606be9f42ead0

```
{
  "question": {
    "answer": "body", 
    "category": 1, 
    "difficulty": 3, 
    "id": 28, 
    "question": "Human machinery"
  }, 
  "success": true
}
```

### POST /users

* General
<<<<<<< HEAD
    * Add Users/Players
    * [URI:-] (http://127.0.0.1:5000/quizzes)
    * Test `curl http://127.0.0.1:5000/users -X POST -H "Content-Type: application/json" -d '{"name": "Lukas"}'`
* Response:
=======
    - Add Users/Players
    - Returns success, and user's name
* Sample: `curl http://127.0.0.1:5000/users -X POST -H "Content-Type: application/json" -d '{"name": "Lukas"}'`
>>>>>>> ce0c1c80925c1e586e2884d82cb606be9f42ead0

```
{
  "name": "Lukas", 
  "success": true
}
```

### PATCH /users

* General
<<<<<<< HEAD
    * Update user's score
    * [URI:-] (http://127.0.0.1:5000/quizzes)
    * Test `curl http://127.0.0.1:5000/users -X PATCH -H "Content-Type: application/json" -d '{"id": 1, "score": 4}'`
* Response:
=======
    - Update user's score
    - Returns success, user_id, score
* Sample: `curl http://127.0.0.1:5000/users -X PATCH -H "Content-Type: application/json" -d '{"id": 1, "score": 4}'`
>>>>>>> ce0c1c80925c1e586e2884d82cb606be9f42ead0

```
{
  "id": 1, 
  "score": 4, 
  "success": true
}
```

### POST /categories

* General
<<<<<<< HEAD
    * Adds Categories
    * [URI:-] (http://127.0.0.1:5000/categories)
    * Test `curl http://127.0.0.1:5000/categories -X POST -H "Content-Type: application/json" -d '{"type": "Fruits"}'`
* Response: 
=======
    - Adds Categories
    - Returns all categories, success, and current type added
* Sample: `curl http://127.0.0.1:5000/categories -X POST -H "Content-Type: application/json" -d '{"type": "Fruits"}'`
>>>>>>> ce0c1c80925c1e586e2884d82cb606be9f42ead0

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports", 
    "7": "Books", 
    "8": "Nature", 
    "9": "Zoos", 
    "10": "Markets", 
    "11": "Fruits"
  }, 
  "success": true, 
  "type": "Fruits"
}
```

## Deployment N/A

### Authors

Ogbuehi I.C, Udacity Team

## Acknowledgements

<<<<<<< HEAD
The awesome team at Udacity, Lectureres, Reviewers, et al.
=======
The awesome team at Udacity, Lectureres, Reviewers, et al.
>>>>>>> ce0c1c80925c1e586e2884d82cb606be9f42ead0
