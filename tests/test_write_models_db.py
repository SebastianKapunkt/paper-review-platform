from flask import Flask
import unittest

from app import db
from app.models import User, Author, Paper, Review


class Test_Write_Models(unittest.TestCase):

    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        self.app = Flask(__name__)
        self.app.config.from_object('app.test_config')
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        with self.app.app_context():
            db.drop_all()

    def test_write_paper(self):
        paper = Paper(
            title="How to conquer the World",
            abstract="just conquer it!",
            status=0
        )

        review = Review()
        author = Author()
        user_that_authored = User()
        user_that_reviews = User()

        user_that_authored.authors.append(author)
        user_that_reviews.reviews.append(review)

        paper.authors.append(author)
        paper.reviews.append(review)

        db.session.add(paper)
        db.session.commit()

        paper = Paper.query.all()[0]
        self.assertEqual(review, paper.reviews[0])
        self.assertEqual(author, paper.authors[0])
        self.assertEqual(user_that_authored, paper.authors[0].user)
        self.assertEqual(user_that_reviews, paper.reviews[0].user)
