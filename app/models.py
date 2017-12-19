from app import db


class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    paper_id = db.Column(db.Integer, db.ForeignKey('papers.id'))
    user = db.relationship("User", back_populates="authors")
    paper = db.relationship("Paper", back_populates="authors")


class Paper(db.Model):
    __tablename__ = 'papers'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    abstract = db.Column(db.String)
    status = db.Column(db.Integer)

    authors = db.relationship("Author", back_populates="paper")
    reviews = db.relationship("Review", back_populates="paper")

    def get_score(self):
        summary = 0;
        reviewd = 0;

        for review in self.reviews:
            if review.score:
                summary += review.score
                reviewd += 1
        if reviewd > 0:
            return round(summary / reviewd, 2)
        else:
            return None;


class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    paper_id = db.Column(db.Integer, db.ForeignKey('papers.id'))
    user = db.relationship("User", back_populates="reviews")
    paper = db.relationship("Paper", back_populates="reviews")


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), unique=True)
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String(), unique=True)
    reset_password_token = db.Column(db.String(), nullable=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())

    role_name = db.Column(db.String(), db.ForeignKey('roles.name'))

    reviews = db.relationship("Review", back_populates="user")
    authors = db.relationship("Author", back_populates="user")


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), unique=True)

    users = db.relationship("User", backref="role",  lazy='dynamic')
