from flask import render_template, flash, redirect, url_for, request, g
from app import app
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Collection
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm, LoginForm, CollectionForm, FilterForm, DeleteForm


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
def route():
    return redirect(url_for('index'))


@app.route('/index', methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = FilterForm()
    if form.validate_on_submit():
        flash('Deals on '+form.filter.data.strftime('%d.%m.%Y'))
        collections = Collection.query.filter_by(user_id=current_user.id, numb=form.filter.data).all()
    else:
        collections = Collection.query.filter_by(user_id=current_user.id).order_by(Collection.numb).all()
    if len(collections) == 0:
        collections = None
    return render_template('index.html', title='Home', collections=collections, form=form)

    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    print('current_user:', current_user)
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/creates1', methods=['GET', 'POST'])
def creates1():
    form = CollectionForm()
    if form.validate_on_submit():
        collection = Collection(name=form.name.data, numb=form.numb.data, user_id=current_user.id)
        #current_user.add_collection(collection)
        db.session.add(collection)
        db.session.commit()
        flash('Congratulations, you added deal "'+str(form.name.data) +
              '" on '+form.numb.data.strftime('%d.%m.%Y')+'!')
        return render_template('creates1.html', title='Collection create', form=form)
    return render_template('creates1.html', title='Collection create', form=form)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    form = DeleteForm()
    if form.validate_on_submit():
        collections = Collection.query.filter_by(user_id=current_user.id, numb=form.numb.data, name=form.name.data).first()
        if collections is None:
            flash('Not found')
        else:
            db.session.delete(collections)
            db.session.commit()
            flash('Congratulations, you deleted deal "'+str(form.name.data) + '" planed on '+form.numb.data.strftime('%d.%m.%Y')+'!')
        return render_template('delete.html', title='Delete', form=form)
    return render_template('delete.html', title='Delete', form=form)
