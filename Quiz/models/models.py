from flask_sqlalchemy import SQLAlchemy
from . import db

class Subject(db.Model):
    __tablename__ = "subjects"
    Subject_id = db.Column(db.String, primary_key=True)
    Subject_name = db.Column(db.String, nullable=False)
    Description = db.Column(db.String(100), nullable=True)
    No_of_chapters_inside = db.Column(db.Integer)
    chapters = db.relationship('Chapter', backref='subject', cascade="all, delete-orphan")


class Chapter(db.Model):
    __tablename__ = "chapter"
    
    Chapter_id = db.Column(db.String, primary_key=True)
    Chapter_name = db.Column(db.String, nullable=False)
    Description = db.Column(db.String(75))
    Subject_id = db.Column(db.String, db.ForeignKey('subjects.Subject_id', ondelete="CASCADE"))
    quizzes = db.relationship('Quiz', backref='chapter', cascade="all, delete-orphan")

class Quiz(db.Model):

    __tablename__ = "quiz"
    Quiz_id = db.Column(db.String, primary_key=True)
    Quiz_name = db.Column(db.String, nullable=False)
    Chapter_id = db.Column(db.String, db.ForeignKey('chapter.Chapter_id', ondelete="CASCADE"))
    Time_duration = db.Column(db.Integer)
    No_of_Questions = db.Column(db.Integer)
    questions = db.relationship('Question', backref='quiz', cascade="all, delete-orphan")


class Question(db.Model):
    __tablename__ = "questions"
    Question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Quiz_id = db.Column(db.String, db.ForeignKey('quiz.Quiz_id', ondelete="CASCADE"))

    Question_Statement = db.Column(db.Text)
    Option1 = db.Column(db.String)
    Option2 = db.Column(db.String)
    Option3 = db.Column(db.String)
    Option4 = db.Column(db.String)

    Correct_option = db.Column(db.String)

class User(db.Model):

    __tablename__ = "user" 
    User_id = db.Column(db.String, primary_key=True)
    Password = db.Column(db.String, nullable=False)
    Name = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    Phone_number = db.Column(db.String(10))
    valid = db.Column(db.Integer, default=1)
    scores = db.relationship('Score', backref='user', cascade="all, delete-orphan")


class Score(db.Model):


    __tablename__ = "scores"
    score_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-increment primary key
    User_id = db.Column(db.Integer, db.ForeignKey('user.User_id', ondelete="CASCADE"), nullable=False)
    Quiz_id = db.Column(db.String, db.ForeignKey('quiz.Quiz_id', ondelete="CASCADE"), nullable=False)
    Score = db.Column(db.Integer)
    Time_taken=db.Column(db.Integer)

class Admin(db.Model):

    __tablename__ = "admin"
    Admin_id = db.Column(db.String, primary_key=True)
    Admin_password = db.Column(db.String)

