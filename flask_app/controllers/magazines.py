from flask_app import app
from flask import session, redirect, render_template, request
from flask_app.models.magazine import Magazine
from flask_app.models.user import User


@app.route('/home/create')
def add_magazine():
    if 'id' not in session:
        return redirect('/')

    return render_template('add_magazine.html')


@app.route('/home/create/new', methods=['POST'])
def new_magazine():
    if not Magazine.validate_post(request.form):
        return redirect('/home/create')

    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'user_id': session['id']
    }
    Magazine.add(data)

    return redirect('/home')


@app.route('/delete/<user_id>-<magazine_id>')
def delete(user_id, magazine_id):
    if not session['id'] == int(user_id):
        return redirect('/')

    data = {
        'id': magazine_id
    }
    Magazine.delete(data)

    return redirect('/home/account')


@app.route('/home/show/<id>')
def show(id):
    if 'id' not in session:
        return redirect('/')

    data = {
        'id': id
    }
    magazine = Magazine.get_magazine(data)

    return render_template('show.html', magazine=magazine)


@app.route('/home')
def home():
    if 'id' not in session:
        return redirect('/')

    magazines = Magazine.get_all()
    user = User.check_email(session)

    return render_template('home.html', magazines=magazines, user=user)
