from app import db
from app.models import User, Author, Paper, Review
import unittest


class Test_Models(unittest.TestCase):

    def test_relation_user_author(self):
        author = Author()
        user = User()
        user.authors.append(author)

        self.assertEqual(author, user.authors[0])
        self.assertEqual(user, author.user)

    def test_relation_author_paper(self):
        author = Author()
        paper = Paper()
        paper.authors.append(author)

        self.assertEqual(author, paper.authors[0])
        self.assertEqual(paper, author.paper)

    def test_relation_user_author_paper(self):
        author = Author()
        user = User()
        paper = Paper()

        user.authors.append(author)
        paper.authors.append(author)

        self.assertEqual(paper, user.authors[0].paper)
        self.assertEqual(user, paper.authors[0].user)

    def test_relation_user_review(self):
        review = Review()
        user = User()
        user.reviews.append(review)

        self.assertEqual(review, user.reviews[0])
        self.assertEqual(user, review.user)

    def test_relation_review_paper(self):
        review = Review()
        paper = Paper()
        paper.reviews.append(review)

        self.assertEqual(review, paper.reviews[0])
        self.assertEqual(paper, review.paper)

    def test_relation_user_review_paper(self):
        review = Review()
        user = User()
        paper = Paper()

        user.reviews.append(review)
        paper.reviews.append(review)

        self.assertEqual(paper, user.reviews[0].paper)
        self.assertEqual(user, paper.reviews[0].user)
        