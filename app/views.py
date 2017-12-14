from flask import render_template, request, redirect, flash, session, url_for
from app import app, db
from app.models import User
from app import user_controller, paper_controller
from app.decorators import login_required


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
        return redirect('/')
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
            return redirect('/')
        else:
            flash('Error wrong Username or Password')
    return render_template('signin.html', title="SignIn")


@app.route('/signout')
@login_required
def logout():
    """Logout the current user."""
    session.clear()
    return redirect("/signin")


@app.route('/')
def root():
    if "logged_in" in session:
        return render_template('welcome.html', title="Papers")
    else:
        return redirect("/signin")


@app.route('/submission')
def submission():
    users = user_controller.get_users()
    return render_template('submission.html', title="Submission", users=users)


@app.route('/paper')
def paper():
    papers = paper_controller.get_papers()
    return render_template('paper.html', title="Paper", papers=papers)


@app.route('/paper/create', methods=['POST'])
def create_paper():
    title = request.form['title']
    abstract = request.form['abstract']
    collaborators = request.form.getlist('collaborators')

    paper_controller.create_paper(title, abstract, collaborators)
    return redirect('/paper')


@app.route('/paper/<int:paper_id>/edit', methods=['POST', 'GET'])
def edit_paper(paper_id):
    if request.method == 'POST':
        title = request.form['title']
        abstract = request.form['abstract']
        collaborators = request.form.getlist('collaborators')
        reviwers = request.form.getlist('reviewer')

        paper_controller.save_paper(
            paper_id, title, abstract, collaborators, reviwers)
        return redirect(url_for('edit_paper', paper_id=paper_id))

    if request.method == 'GET':
        all_user = user_controller.list()
        print("all user")
        print(all_user)
        paper = paper_controller.get(paper_id)
        filtered_user = paper_controller.filter_resolved_user(paper, all_user)

        return render_template(
            'edit_paper.html',
            title=paper.title,
            paper=paper,
            filtered_user=filtered_user
        )
