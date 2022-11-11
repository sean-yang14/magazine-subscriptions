from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

db = 'magazine'


class Magazine:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.author = None
        self.user_id = data['user_id']

    @staticmethod
    def validate_post(data):
        is_valid = True

        if not data['title'] or not data['description']:
            flash('All fields must be filled out')
            is_valid = False

        if len(data['title']) < 2:
            flash('Title must be at least 2 characters long')
            is_valid = False

        if len(data['description']) < 10:
            flash('Description must be at least 10 characters long')
            is_valid = False

        return is_valid

    @classmethod
    def add(cls, data):
        query = 'INSERT INTO magazines (title, description, user_id) VALUES (%(title)s, %(description)s, %(user_id)s);'

        connectToMySQL(db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM magazines WHERE id=%(id)s'
        connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_magazine(cls, data):
        query = 'SELECT * FROM magazines JOIN users ON user_id=users.id WHERE magazines.id=%(id)s;'
        results = connectToMySQL(db).query_db(query, data)
        result = results[0]

        data = {
            'id': result['users.id'],
            'first_name': result['first_name'],
            'last_name': result['last_name'],
            'email': result['email'],
        }
        magazine = cls(result)
        magazine.author = user.User(data)

        return magazine

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM magazines JOIN users ON user_id=users.id;'
        results = connectToMySQL(db).query_db(query)
        magazines = []

        for i in results:
            data = {
                'id': i['users.id'],
                'first_name': i['first_name'],
                'last_name': i['last_name'],
                'email': i['email'],
            }
            magazine = cls(i)
            magazine.author = user.User(data)
            magazines.append(magazine)

        return magazines
