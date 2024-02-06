from  flask import Blueprint,redirect,render_template,request,flash,url_for
from flask_login import login_required,current_user
from .models import Course,Lesson,Comment
from . import db


views = Blueprint('views', __name__)

@views.route('/home',methods=['GET','POST'])
@login_required
def home():
    
    if current_user.email == 'sdgiri0662@gmail.com':
               return render_template('admin.html',user = current_user)
    else:
         return render_template('home.html',user = current_user)    
    

@views.route('/view_courses')
@login_required
def view_courses():
    courses = Course.query.all()
    return render_template('view_courses.html',courses=courses)

@views.route('/update_courses',methods = ['GET','POST'])
@login_required
def update_courses():
    if request.method == 'POST':
          course_id = request.form.get('course_id')
          course_name = request.form.get('course_name')
          introduction = request.form.get('introduction')
          course = Course.query.filter_by(id = course_id).first()
          if course:
               course.course_name = course_name
               course.introduction = introduction
               db.session.commit()
               flash("Course detalis updated!", category='success')
               return render_template('update_courses.html')
          else:
               if len(course_name)<3:
                    flash("please enter a valid course name",category='error')
               new_data = Course(course_name=course_name,introduction = introduction)
               db.session.add(new_data)
               db.session.commit()
               flash("New Course Added!", category='success')
               return render_template('update_courses.html')
    else:
         return render_template('update_courses.html')
        
@views.route('/view_lessons')
@login_required
def view_lessons():
    course_id = request.args.get('course_id')
    lessons = Lesson.query.filter_by(course_id = course_id).all()
    course = Course.query.filter_by(id = course_id).first()

    return render_template('view_lessons.html',lessons=lessons,course=course)

@views.route('/view_lesson_details')
@login_required
def view_lesson_details():
    lesson_id = request.args.get('lesson_id')
    lesson = Lesson.query.filter_by(id = lesson_id).first()
    comments = Comment.query.filter_by(lesson_id = lesson_id).all()
    return render_template('view_lesson_details.html', lesson =lesson,comments =comments)

@views.route('/add_lessons',methods = ['GET','POST'])
@login_required
def add_lessons():
    if request.method == 'GET':
        return render_template('add_lessons.html')
    else:
        lesson_name = request.form.get('lesson_name')
        course_id = request.form.get('course_id')
        video_link = request.form.get('video_link')
        if len(lesson_name) < 4:
             flash("please enter a valid lesson name", category='error')
             return redirect(url_for(views.add_lessons))
        elif len(video_link) < 5:
             flash("please enter a valid Video link", category='error')
             return redirect(url_for(views.add_lessons))
        new_data = Lesson(lesson_name = lesson_name, course_id = course_id ,video_link = video_link)
        db.session.add(new_data)
        db.session.commit()
        flash("Data Inserted Successfully", category='success')
        return redirect(url_for('views.add_lessons'))

@views.route('/add_comment',methods = ['GET','POST'])
@login_required
def add_comment():
    if request.method == 'POST':
        lesson_id = request.args.get('lesson_id')
        text = request.form.get('text')
        user_id = current_user.id

        new_comment = Comment(text = text, user_id = user_id, lesson_id = lesson_id)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("views.view_lesson_details", lesson_id = lesson_id))
