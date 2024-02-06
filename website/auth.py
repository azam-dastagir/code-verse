from flask import Blueprint,request,render_template,redirect,url_for, flash
from flask_login import login_user,logout_user,login_required,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User,Course,Lesson
from .import db



auth = Blueprint('auth',__name__)



@auth.route('/',methods=['GET','POST'])
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', user=current_user)

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user:
            try:
                if check_password_hash(user.password, password):
                    login_user(user=user, remember=True)
                    flash("Login Successful!", category="success")
                    return redirect(url_for("views.home", user=current_user))
                else:
                    flash("Wrong password, please try again!", category='error')
                    return redirect(url_for("auth.login"))  # Return to login page on failure
            except Exception as e:
                flash("An error occurred while checking the password.", category='error')
                return redirect(url_for("auth.login"))  # Return to login page on error
        else:
            flash("Email doesn't exist", category='error')
            return redirect(url_for("auth.login"))  # Return to login page on failure
        
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('sign_up.html', user=current_user)

    try:
        email = request.form.get('email')
        name = request.form.get('first_name')
        password = request.form.get('password')
        cnfm_password = request.form.get('cnfm_password')

        if password != cnfm_password:
            flash("Passwords do not match, please enter again!", category='error')
        elif len(password) < 6:
            flash("Password length should be at least 6 characters", category='error')
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            login_user(user=new_user, remember=True)
            flash('Account Created!', category="success")
            return redirect(url_for('views.home', user=current_user))

    except Exception as e:
        # Handle other exceptions or log them as needed
        flash(f"An error occurred: {str(e)}", category='error')

    return redirect(url_for('auth.signup'))

          
@auth.route('/logout')
@login_required
def logout():
   logout_user()
   return redirect(url_for('auth.login'))