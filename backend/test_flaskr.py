import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, db


database_username = os.environ['DB_USER']
database_password = os.environ['DB_PASSWORD']
db_host = os.environ['DB_HOST']
db_port = os.environ['DB_PORT']
database_name = os.environ['DB_NAME_TEST']

database_path = 'postgresql://{}:{}@{}:{}/{}'.format(
    database_username,
    database_password,
    db_host,
    db_port,
    database_name
)

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        self.database_path = database_path
        
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })

        self.client = self.app.test_client

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


    ####
    # Testing
    ####
    ####

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(len(data["categories"]))

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertEqual(data["current_category"], '')
        self.assertTrue(data["categories"])

    def test_delete_questions(self):
        res = self.client().delete("/questions/2")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(question, None)
    
    def test_delete_questions_not_found(self):
        res = self.client().delete("/questions/200")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["messages"], "Unprocessable entity")

    def test_create_new_question(self):
        res = self.client().post("/questions", json={
            "question": "New question",
            "answer": "New answer",
            "difficulty": 10,
            "category": 2
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_search_questions(self):
        res = self.client().post("/questions/search", json={
            "query": "question"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertEqual(data["current_category"], "")

    def test_search_questions_by_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["current_category"])

    def test_search_questions_by_category_not_found(self):
        res = self.client().get("/categories/100/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["messages"], "Unprocessable entity")

    def test_get_quiz_question(self):
        res = self.client().post("/quizzes", json={
            "previous_questions": [],
            "category_id": 2
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["question"])

    def test_get_url_notfound(self):
        res = self.client().get("/test-url")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Page not found")
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()