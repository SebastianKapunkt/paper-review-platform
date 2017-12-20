from flask import session
from app import app, db
from app.models import Paper, Author, User, Review


class Paper_Controller:
    def create_paper(self, title, abstract, collaborators):
        new_paper = Paper(
            title=title,
            abstract=abstract,
            status=0
        )

        for collaborator in collaborators:
            author = Author()
            author.user = User.query.get(int(collaborator))
            new_paper.authors.append(author)

        if not collaborators:
            author = Author()
            author.user = User.query.get(session['user_id'])
            new_paper.authors.append(author)

        db.session.add(new_paper)
        db.session.commit()

    def get_papers(self):
        papers = Paper.query.all()
        return papers[::-1]

    def get(self, paper_id):
        return Paper.query.get(paper_id)

    def is_reviewer(self, paper, user_id):
        is_reviewer = False
        for review in paper.reviews:
            if review.user.id == user_id:
                is_reviewer = True
        return is_reviewer

    def is_author(self, paper, user_id):
        is_author = False
        for author in paper.authors:
            if author.user.id == user_id:
                is_author = True
        return is_author

    def get_review(self, paper, user_id):
        user_review = None
        for review in paper.reviews:
            if review.user.id == user_id:
                user_review = review
        return user_review

    def apply_rating(self, paper, user_id, rating):
        review = self.get_review(paper, user_id)
        review.score = rating
        db.session.commit()
        return review

    def get_papers_auhtored_by_user(self, user_id):
        papers = self.get_papers()
        authored = []
        for paper in papers:
            if self.is_author(paper, user_id):
                authored.append(paper)
        return authored

    def get_papers_to_review_by_user(self, user_id):
        papers = self.get_papers()
        to_review = []
        for paper in papers:
            if self.is_reviewer(paper, user_id):
                review = self.get_review(paper, user_id)
                to_review.append({'paper': paper, 'score': review.score})
        return to_review

    def save_paper(self, paper_id, title, abstract, collaborators, reviewer):
        paper = Paper.query.get(paper_id)

        if title:
            paper.title = title
        if abstract:
            paper.abstract = abstract
        if collaborators:
            self.merge_authors(paper, collaborators)
        if reviewer:
            self.merge_reviewer(paper, reviewer)

        db.session.commit()

    def merge_authors(self, paper, collaborators):
        def author_query(user_id): return (
            Author.query.filter_by(
                user_id=user_id,
                paper_id=paper.id
            ).first())

        new_author = (lambda: Author())

        self.merge_generic(paper, collaborators, paper.authors,
                           author_query, new_author)

    def merge_reviewer(self, paper, reviewer):
        review_query = (lambda user_id:
                        Review.query.filter_by(
                            user_id=user_id,
                            paper_id=paper.id
                        ).first())

        new_review = (lambda: Review())

        self.merge_generic(paper, reviewer, paper.reviews,
                           review_query, new_review)

    def merge_generic(self, paper, ids_from_post, current_items, query, item_constructor):
        new_items = []

        for item in ids_from_post:
            new_item = query(item)
            if new_item is None:
                new_item = item_constructor()
                new_item.user = User.query.get(item)
                new_item.paper = paper
            new_items.append(new_item)

        to_delete = list(set(current_items) - set(new_items))
        for item in to_delete:
            db.session.delete(item)

        to_add = list(set(new_items) - set(current_items))
        for item in to_add:
            db.session.add(item)

    def filter_resolved_user(self, paper, all_user):
        reviews_user = self.get_user_of_authors_or_revwies(paper.reviews)
        can_review = list(set(all_user) - set(reviews_user))

        author_user = self.get_user_of_authors_or_revwies(paper.authors)
        can_review = list(set(can_review) - set(author_user))

        return can_review

    def get_user_of_authors_or_revwies(self, items):
        authors_user = []
        for author in items:
            authors_user.append(author.user)
        return authors_user

    def set_paper_status(self, paper, status):   
        paper.status = status
        db.session.commit()
