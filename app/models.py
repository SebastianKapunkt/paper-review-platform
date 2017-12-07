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
    id = db.Column(db.Integer, primary_key=True)
    authors = db.relationship("Author", back_populates="user")
    reviews = db.relationship("Review", back_populates="user")
