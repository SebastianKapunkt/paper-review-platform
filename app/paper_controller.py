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

        db.session.add(new_paper)
        db.session.commit()

    def get_papers(self):
        return Paper.query.all()

    def get(self, paper_id):
        return Paper.query.get(paper_id)

    def save_paper(self, paper_id, title, abstract, collaborators, reviewer):
        paper = Paper.query.get(paper_id)

        paper.title = title
        paper.abstract = abstract

        self.merge_authors(paper, collaborators)
        self.merge_reviewer(paper, reviewer)

        db.session.commit()

    def merge_authors(self, paper, collaborators):
        def author_query(user_id): return (
            Author.query.filter_by(
                user_id=user_id,
                paper_id=paper.id
            ).first())

        new_author = (lambda: Author())

        print("-- authors --")
        self.merge_generic(paper, collaborators, paper.authors,
                           author_query, new_author)

    def merge_reviewer(self, paper, reviewer):
        review_query = (lambda user_id:
                        Review.query.filter_by(
                            user_id=user_id,
                            paper_id=paper.id
                        ).first())

        new_review = (lambda: Review())

        print("-- reviewer --")
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
