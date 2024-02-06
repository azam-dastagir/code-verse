from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model,UserMixin):
     id = db.Column(db.Integer, primary_key = True)
     name = db.Column(db.String(150))
     email = db.Column(db.String(150), unique=True)
     password = db.Column(db.String(150))
     courses = db.relationship("Course" ,backref = "user", passive_deletes = True)
     comments = db.relationship("Comment", backref = "user", passive_deletes = True)
     

class Course(db.Model):
     id = db.Column(db.Integer, primary_key = True)
     course_name = db.Column(db.String(150))
     student_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable = True)
     lessons = db.relationship("Lesson", backref = "course", passive_deletes = True)
     introduction = db.Column(db.String(500))

class Lesson(db.Model):
     id = db.Column(db.Integer, primary_key = True)
     lesson_name = db.Column(db.String(150))
     course_id = db.Column(db.Integer, db.ForeignKey("course.id", ondelete="CASCADE"),nullable = False)
     video_link = db.Column(db.String(250))
     comments = db.relationship("Comment", backref = "lesson", passive_deletes = True)

class Comment(db.Model):
     id = db.Column(db.Integer, primary_key = True)
     text = db.Column(db.String(300))
     date_created = db.Column(db.DateTime(timezone=True),default = func.now())
     user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete = "CASCADE"), nullable = False)
     lesson_id = db.Column(db.Integer, db.ForeignKey("lesson.id", ondelete="CASCADE"), nullable = False)

