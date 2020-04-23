from flask import request, redirect, render_template, flash, url_for
from datetime import datetime

from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, db
from models import Event, User
from forms import EventForm, LoginForm, CreateUserForm


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    email = request.form.get('email')
    password = request.form.get('password')

    if email and password:
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            # return redirect(next_page)
            return redirect(url_for('index'))
        else:
            flash('Email or password is not correct.')
    
    else:
        flash('Please fill email and password.')
    
    return render_template('login.html', form=form)


@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    form = CreateUserForm()
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        
        if not email or not password or not password2 or not name:
            flash('Please fill all fields.')
        elif password != password2:
            flash('Passwords are not equal.')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(name=name, email=email, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login_page'))

    return render_template('register.html', form=form)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
@login_required
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)
    

@app.route('/<int:id>')
@login_required
def event_detail(id):

    event = Event.query.filter(Event.id==id).first_or_404()
    user = event.user.first()
    
    if user.id == current_user.id:
        return render_template('event_detail.html', event=event)

    events = Event.query.all()
    flash('Please login another user.')
    return render_template('index.html', events=events)


@app.route('/save_event', methods=['POST', 'GET'])
@login_required
def save_event():
    event_form = EventForm()

    if request.method == 'POST':
        author = current_user.name
        user = current_user
        date_begin = request.form.get('date_begin')
        date_begin = datetime.strptime(date_begin, '%Y-%m-%d')
        date_end = request.form.get('date_end')
        date_end = datetime.strptime(date_end, '%Y-%m-%d')
        theme = request.form.get('theme')
        description = request.form.get('description')
        event = Event(author=author, date_begin=date_begin, date_end=date_end, theme=theme, description=description)
        event.user.append(user)
        db.session.add(event)
        db.session.commit()
        return redirect('/')
    return render_template('add_event.html', form=event_form)


@app.route('/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    event = Event.query.filter(Event.id==id).first_or_404()
    user = event.user.first()

    if user.id == current_user.id:

        if request.method == 'POST':
            form = EventForm(formdata=request.form, obj=event)
        
            date_begin = request.form.get('date_begin')
            date_end = request.form.get('date_end')
            theme = request.form.get('theme')
            description = request.form.get('description')
            event.date_begin = date_begin
            event.date_end = date_end
            event.theme = theme
            event.description = description

            db.session.commit()
            return redirect(url_for('event_detail', id=event.id))
        
        form = EventForm(obj=event)
        return render_template('edit_event.html', form=form, event=event)

    events = Event.query.all()
    flash('Please login another user.')
    return render_template('index.html', events=events)

@app.route('/<id>/delete')
@login_required
def delete_event(id):
    event = Event.query.filter(Event.id==id).first_or_404()
    user = event.user.first()

    if user.id == current_user.id:
        db.session.delete(event)
        db.session.commit()
        return redirect(url_for('index'))

    events = Event.query.all()
    flash('Please login another user.')
    return render_template('index.html', events=events)


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)

    return response