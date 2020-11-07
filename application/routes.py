from flask import render_template, url_for, flash, redirect, request, session, escape
from application import app, db, bcrypt
from application.forms import RegistrationForm, LoginForm
from application.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
@app.route('/posts')
def index():
    post = Post.query.order_by(Post.date.desc()).all()
    return render_template('posts.html', post=post)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # email = request.form['email']
        # session['email'] = email
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        session['email'] = request.form['email']
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = request.form['email']
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    session.pop('email', None)
    return redirect(url_for('index'))


@app.route('/posts/<int:id>')
@login_required
def detail_post(id):
    details = Post.query.get(id)
    return render_template('details.html', details=details)


@app.route('/posts/<int:id>/del')
@login_required
def posts_details(id):
    details = Post.query.get_or_404(id)

    try:
        db.session.delete(details)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении произошла ошика"


@app.route('/posts/<int:id>/update', methods=['GET', 'POST'])
@login_required
def post_update(id):
    details = Post.query.get(id)
    if request.method == 'POST':
        details.title = request.form.get('title')
        details.text = request.form.get('text')

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При редактировании произошла ошибка'

    else:
        return render_template('post_update.html', details=details)


@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')


@app.route('/post-add', methods=['GET', 'POST'])
@login_required
def adding_post():
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')
        user_id = current_user.id
        value = Post(title=title, text=text, user_id=user_id)
        try:
            db.session.add(value)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При добавлении произошла ошибка'

    else:
        return render_template('post-add.html')
