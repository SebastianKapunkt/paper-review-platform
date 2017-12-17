from flask import render_template, request, redirect, flash, session, url_for
from app import app, db
from app.models import User
from app import user_controller, paper_controller, role_controller
from app.decorators import login_required, requires_roles


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
        user_document = user_controller.authenticate_user(email, password)

        if user_document:
            flash('You have been logged in!')
            session['logged_in'] = True
            session['username'] = user_document['username']
            session['user_id'] = user_document['id']
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
@login_required
def submission():
    users = user_controller.get_users()
    return render_template('submission.html', title="Submission", users=users)


@app.route('/paper')
@login_required
def paper():
    papers = paper_controller.get_papers()
    return render_template('paper.html', title="Paper", papers=papers)


@app.route('/paper/create', methods=['POST'])
@login_required
def create_paper():
    title = request.form['title']
    abstract = request.form['abstract']
    collaborators = request.form.getlist('collaborators')

    paper_controller.create_paper(title, abstract, collaborators)
    return redirect('/paper')


@app.route('/paper/<int:paper_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_paper(paper_id):
    if request.method == 'POST':
        title = request.form['title']
        abstract = request.form['abstract']
        submit = request.form['submit']
        collaborators = request.form.getlist('collaborators')
        reviwers = request.form.getlist('reviewer')

        if(submit != "cancel"):
            paper_controller.save_paper(
                paper_id, title, abstract, collaborators, reviwers)

        if(submit == "redirect"):
            return redirect(url_for('edit_paper', paper_id=paper_id))
        else:
            return redirect(url_for('show_paper', paper_id=paper_id))

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


@app.route('/paper/<int:paper_id>/', methods=['GET'])
@login_required
def show_paper(paper_id):
    if request.method == 'GET':
        paper = paper_controller.get(paper_id)

        return render_template(
            'show_paper.html',
            title=paper.title,
            paper=paper
        )
@app.route('/admin', methods=['GET'])
@login_required
@requires_roles('admin')
def admin_page():
    users = user_controller.get_users()
    roles = role_controller.get_roles()
    return render_template('admin.html', title="Admin", users=users, roles=roles)

@app.route('/admin/set-role', methods=['POST'])
@login_required
@requires_roles('admin')
def set_roles():
    user_ids = request.form.getlist('user_ids')
    role = request.form['role']
    user_controller.set_user_role(user_ids, role)
    return redirect('/admin')
