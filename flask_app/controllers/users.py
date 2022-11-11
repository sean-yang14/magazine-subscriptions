from flask_app import app
from flask import session, redirect, render_template, flash, request
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    if 'id' in session:
        return redirect('/home')
    return redirect('/register_login')


@app.route('/register_login')
def register_login():
    return render_template('register_login.html')


@app.route('/register_login/register', methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')

    # hash password and send data to User class to add to database
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    User.register_user(data)

    user = User.get_user(data)
    session['id'] = user['id']
    session['first_name'] = user['first_name']
    session['last_name'] = user['last_name']

    return redirect('/home')


@app.route('/register_login/login', methods=['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')

    user = User.get_user(request.form)

    if not user:
        flash('Email not found')
        return redirect('/')

    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash('Incorrect password')
        return redirect('/')

    session['id'] = user['id']
    session['first_name'] = user['first_name']
    session['last_name'] = user['last_name']

    return redirect('/home')


@app.route('/home/account')
def account():
    if 'id' not in session:
        return redirect('/')

    user = User.get_user_update(session)
    return render_template('account.html', user=user)


@app.route('/update_user', methods=['POST'])
def update_user():
    if not User.validate_update(request.form):
        return redirect('/home/account')

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'id': session['id']
    }
    User.update_user(data)
    flash('Update successful')

    return redirect('/home/account')


@app.route('/logout')
def logout():
    if 'id' not in session:
        return redirect('/')

    session.clear()
    return redirect('/')
