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

        state = user_controller.create_user(
            username, email.lower(), password, first_name, last_name)

        if state == 'ok':
            flash(
                'Welcome to Paper-Reviewer {username} ,you have successfuly registered')
            return redirect('/')
        else:
            return render_template('signup.html', title="SignUp", form=request.form)

    return render_template('signup.html', title="SignUp", form=request.form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    """renders the signin form when /signin is called"""
    error = None
    if request.method == "POST":
        email = request.form['email'].lower()
        password = request.form['password']
        user_dict = user_controller.authenticate_user(email, password)

        if user_dict:
            flash('You have been logged in!')
            session['logged_in'] = True
            session['username'] = user_dict['username']
            session['user_id'] = user_dict['user_id']
            session['role'] = user_dict['role']
            return redirect('/')
        else:
            error = 'Error wrong Username or Password'
    return render_template('signin.html', title="SignIn", error=error)


@app.route('/signout')
@login_required
def logout():
    """Logout the current user."""
    session.clear()
    return redirect("/signin")


@app.route('/')
def root():
    if "logged_in" in session:
        return redirect(url_for('to_review_by_user'))
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
    paper = paper_controller.get(paper_id)
    if not paper_controller.is_author(paper, session['user_id']):
        return redirect(url_for('show_paper', paper_id=paper_id))

    if request.method == 'POST':
        title = request.form['title']
        abstract = request.form['abstract']
        submit = request.form['submit']
        collaborators = request.form.getlist('collaborators')

        if(submit != "cancel"):
            paper_controller.save_paper(
                paper_id,
                title,
                abstract,
                collaborators,
                None
            )

        if(submit == "redirect"):
            return redirect(url_for('edit_paper', paper_id=paper_id))
        else:
            return redirect(url_for('show_paper', paper_id=paper_id))

    if request.method == 'GET':
        all_user = user_controller.list()
        filtered_user = paper_controller.filter_resolved_user(
            paper,
            all_user
        )

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
        can_edit = paper_controller.is_author(paper, session['user_id'])
        return render_template(
            'show_paper.html',
            title=paper.title,
            paper=paper,
            can_edit=can_edit
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


@app.route('/paper/<int:paper_id>/review', methods=['POST', 'GET'])
@login_required
def review_paper(paper_id):
    paper = paper_controller.get(paper_id)
    if paper_controller.is_reviewer(paper, session['user_id']):
        if request.method == 'GET':
            if paper_controller.is_reviewer(paper, session['user_id']):
                review = paper_controller.get_review(paper, session['user_id'])
                return render_template(
                    'review_paper.html',
                    title=paper.title,
                    paper=paper,
                    review=review
                )

        if request.method == 'POST':
            rating = request.form['rating']
            submit = request.form['submit']
            review = paper_controller.apply_rating(
                paper,
                session['user_id'],
                rating
            )
            if submit == "redirect":
                return redirect(url_for('to_review_by_user'))
            else:
                return redirect(url_for('review_paper', paper_id=paper.id))
    else:
        return redirect('/')


@app.route('/authored', methods=['GET'])
@login_required
def authored_by_user():
    papers = paper_controller.get_papers_auhtored_by_user(session['user_id'])
    return render_template('user_authored.html', title="Paper", papers=papers)


@app.route('/to_review', methods=['GET'])
@login_required
def to_review_by_user():
    papers = paper_controller.get_papers_to_review_by_user(session['user_id'])
    return render_template('to_review.html', title="Paper", papers=papers)


@app.route('/conference_chair', methods=['GET'])
@login_required
@requires_roles('council', 'admin')
def conference_chair():
    papers = paper_controller.get_papers()
    return render_template('chair.html', title="Conference Chair", papers=papers)


@app.route('/paper/<int:paper_id>/council/edit', methods=['GET', 'POST'])
@login_required
@requires_roles('council', 'admin')
def council_edit_paper(paper_id):
    paper = paper_controller.get(paper_id)
    if request.method == 'GET':
        all_user = user_controller.list()
        filtered_user = paper_controller.filter_resolved_user(
            paper,
            all_user
        )
        return render_template(
            'council_edit_paper.html',
            title="Conference Chair",
            paper=paper,
            filtered_user=filtered_user
        )
    if request.method == 'POST':
        submit = request.form['submit']
        reviwers = request.form.getlist('reviewer')

        if(submit != "cancel"):
            paper_controller.save_paper(
                paper_id,
                None,
                None,
                None,
                reviwers
            )

        if(submit == 'approve'):
            paper_controller.set_paper_status(paper, 2)
        elif(submit == 'reject'):
            paper_controller.set_paper_status(paper, 1)

        if(submit == "redirect"):
            return redirect(url_for('conference_chair'))
        else:
            return redirect(url_for('council_edit_paper', paper_id=paper_id))
        