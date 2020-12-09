# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```

API REFERENCE
Error Handling
Errors are returned as JSON objects in the following format.

{
    "success": False,
    "error": 400,
    "message": "bad request"
}

The API will return three error types when request fail:
- 400: Bad Request
- 404: Resource not found
- 405: Method not allowed
- 422: Unprocessable entity
- 500: Internal server error

### Endpoints
GET '/categories'
GET '/questions'
GET '/categories/<int:id>/questions'
POST '/questions'
POST '/questions/search'
POST '/quizzes'
DELETE '/questions/<int:id>'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
- Fetches a dictionary with categories, in which the keys are the ids and the value is the corresponding string of the category. 
Also the dictionary have paginated questions, only shows 10 questions per page, in which the keys are the information of the question. 
Finaly has the number of total questions. 
- Request Arguments: Query string parameter
    - page: the number of the page, only shows 10 questions per page
    - example: http://127.0.0.1:5000/questions?page=3
- Returns: An object with categories, that contains an object of id: category_string key:value pairs.
    Also shows questions in a array, that contains objects with the next keys:
    - id: (int) the id of the object
    - category: (String) the category of the questions
    - difficulty: (int) the lv of the question difficulty
    - question: (String) the question of the quizz
    - answer: (String) the answer of the question
{
    "categories": {
        "1": "science",
        "2": "art",
        "3": "geography",
        "4": "history",
        "5": "entertainment",
        "6": "sports"
    },
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
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
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
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
    "total_questions": 19
}
GET '/categories/<int:id>/questions'
- Fetches questions by categories, also fetch the information of the current category(type of category), and finaly the total questions found it.
- Request arguments: Path parameter
    - "/categories/<int:id>/questions": it has to be put the id of the category to get all the questions of that category.
    - example: http://127.0.0.1:5000/categories/1/questions
- Returns: Returns an object  with the current_category:
            - id: (int) id of the category selected.
            - type: (string) type of the category.
            Also shows an array of questions fetched by the category with the next keys.
            - id: (int) the id of the object
            - category: (String) the category of the questions
            - difficulty: (int) the lv of the question difficulty
            - question: (String) the question of the quizz
            - answer: (String) the answer of the question

{
    "current_category": {
        "id": 1,
        "type": "Science"
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
        }
    ],
    "success": true,
    "total_questions": 3
}
POST '/questions'
- Create a new question with the data provided through request body and returns a dictionary with the id of the created question, and if the request was success.
- Request arguments: Request body JSON
    - question: (String) The question for the quizz.
    - answer: (String) The answer for the question.
    - category: (Int) the id of the category of this question
    - difficulty: (Int) the lv of the difficulty from 1 to 5.
- Returns: Returns an object with the next Keys
    - "created": (int) the id of the created question
    - "success": (boolean) True if the question was created successfully or False if had a problem. 
{
    "created": 25,
    "success": true
}

POST '/questions/search'
- Fetches all the questions that match with the search_term provided 
- Request arguments: Request body JSON
    - searchTerm: (String) The search term to find the questions.
- Returns: Return an object with the current category:
    - "current_category": (String) the current category selected.
    - "questions": (array of questions) with the next keys:
        - id: (int) the id of the object
        - category: (String) the category of the questions
        - difficulty: (int) the lv of the question difficulty
        - question: (String) the question of the quizz
        - answer: (String) the answer of the question
{
    "current_category": null,
    "questions": [
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Avengers: Endgame",
            "category": 5,
            "difficulty": 3,
            "id": 24,
            "question": "What is the highest-grossing film of all time without taking inflation into account?"
        }
    ],
    "success": true,
    "total_questions": 3
}
POST '/quizzes'
- Fetches randomly questions to play the trivia of a specific category provided.
- Request arguments: Request body JSON
    The first parameter that needs this API is the quiz_category, with the keys of id of the category and the type of category.
    If the id is 0,It means that is selected to play with all the categories.
    It also needs to add the "previous_questions", is an array of the IDs of the questions that was asked to the quizz, if the "previous_questions" is an empty array it means that there weren't questions asked previously, if it has Ids it means that those id are the questions asked before, and those questions won't be asked again.
    Example:
    {
    "quiz_category": {
        "id":0,
        "type":"All"
    },
    "previous_questions":[]
}
- Returns: Returns an object with the category selected to play the quizz,
    Also the random question of that category with the next keys:
        - id: (int) the id of the object
        - category: (String) the category of the questions
        - difficulty: (int) the lv of the question difficulty
        - question: (String) the question of the quizz
        - answer: (String) the answer of the question
    If the question is null means that there is no more questions, and the quizz ended.
{
    "category": {
        "id": 0,
        "type": "All"
    },
    "question": {
        "answer": "Jackson Pollock",
        "category": 2,
        "difficulty": 2,
        "id": 19,
        "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    "success": true
}

DELETE '/questions/<int:id>'
- Delete a question with an id provided by the user.
- Request arguments: Path parameters
    -  /questions/<int:id>: It needs the id of the question to delete it.
    - example: http://127.0.0.1:5000/questions/25
- Returns: returns an object with the next keys
        - "deleted": (Int) "The id of the deleted question"
        - "success": (boolean) True if the question was deleted successfully or False if had a problem.
{
    "deleted": 25,
    "success": true
}
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```