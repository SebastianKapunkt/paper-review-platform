from app import app, db
from app.models import Paper, Author, User


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
