from app import app, db
from app.models import Paper


class Paper_Controller:
    def create_paper(self, title, abstract):
        new_paper = Paper(
            title=title,
            abstract=abstract,
            status=0
        )

        db.session.add(new_paper)
        db.session.commit()

    def get_papers(self):
        return Paper.query.all()
