from flask import render_template, request, redirect, flash, session
from app import app, db
from app.models import User
from app import user_controller, paper_controller
from app.decorators import login_required


@app.route('/index')
def index():
    return render_template('index.html', title="Home")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """renders the signup form when /signup is called"""

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email'].lower()
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        user_controller.create_user(
            username, email.lower(), password, first_name, last_name)
        flash(
            'Welcome to Paper-Reviewer {username} ,you have successfuly registered')
        return redirect('/index')
    else:
        flash('Please make sure to enter all required Fields')
        return render_template('signup.html', title="SignUp", form=request.form)

    return render_template('signup.html', title="SignUp", form=request.form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    """renders the signin form when /signin is called"""
    if request.method == "POST":
        email = request.form['email'].lower()
        password = request.form['password']
        username = user_controller.authenticate_user(email, password)

        if username:
            flash('You have been logged in!')
            session['logged_in'] = True
            session['username'] = username
            return redirect('/test')
        else:
            flash('Error wrong Username or Password')
    return render_template('signin.html', title="SignIn")


@app.route("/signout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    session.clear()
    return redirect("/index")


@app.route('/test', methods=['GET'])
@login_required
def test():
    """ Some test page to see if login works """
    flash('Welcome on the Test page')
    return render_template('test.html')


@app.route('/')
def root():
    return render_template('nav_bar.html', title="Home")


@app.route('/submission')
def submission():
    return render_template('submission.html', title="Submission")


@app.route('/paper')
def paper():
    papers = paper_controller.get_papers()
    return render_template('paper.html', title="Paper", papers=papers)


@app.route('/paper/create', methods=['POST'])
def create_paper():
    title = request.form['title']
    abstract = request.form['abstract']

    paper_controller.create_paper(title, abstract)
    return redirect('/paper')
