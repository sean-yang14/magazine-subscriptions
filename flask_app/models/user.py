from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import magazine
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

db = 'magazine'


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.magazines = []

    @staticmethod
    def validate_registration(data):
        is_valid = True

        # all fields must be filled out
        if not data['first_name'] or not data['last_name'] or not data['email'] or not data['password'] or not data['confirm']:
            flash('All fields must be filled out')
            is_valid = False

        # check length of names
        if len(data['first_name']) < 3 or len(data['last_name']) < 3:
            flash('Length of names must be at least 3 characters')
            is_valid = False

        # check email logic
        if data['email']:

            # check if email is in the correct format
            if not EMAIL_REGEX.match(data['email']):
                flash('Invalid email format')
                is_valid = False

            # check if email already exists in database
            if User.get_user(data):
                flash('Email already in use')
                is_valid = False

        # password must be min 8 characters
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters')
            is_valid = False

        # check if password and confirmation match
        if not data['password'] == data['confirm']:
            flash('Password and confirm password do not match')
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(data):
        is_valid = True

        if not data['email'] or not data['password']:
            flash('All fields must be filled out')
            is_valid = False

        return is_valid

    @staticmethod
    def validate_update(data):
        is_valid = True

        # all fields must be filled out
        if not data['first_name'] or not data['last_name'] or not data['email']:
            flash('All fields must be filled out')
            is_valid = False

        # check length of names
        if len(data['first_name']) < 3 or len(data['last_name']) < 3:
            flash('Length of names must be at least 3 characters')
            is_valid = False

        # check email logic
        if data['email']:
            # check if email is in the correct format
            if not EMAIL_REGEX.match(data['email']):
                flash('Invalid email format')
                is_valid = False

            # check if email already exists in database
            user = User.check_email(session)
            if not user['email'] == data['email']:
                if User.get_user(data):
                    flash('Email already in use')
                    is_valid = False

        return is_valid

    @classmethod
    def get_user(cls, data):
        query = 'SELECT * FROM users WHERE email=%(email)s;'
        result = connectToMySQL(db).query_db(query, data)

        if result:
            return result[0]

    @classmethod
    def register_user(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'

        connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_user_update(cls, data):
        query = 'SELECT * FROM users LEFT JOIN magazines ON users.id=user_id WHERE users.id=%(id)s;'

        results = connectToMySQL(db).query_db(query, data)
        user = cls(results[0])

        for i in results:
            data = {
                'id': i['magazines.id'],
                'title': i['title'],
                'description': i['description'],
                'user_id': i['user_id']
            }

            user.magazines.append(magazine.Magazine(data))

        return user

    @classmethod
    def update_user(cls, data):
        query = 'UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s WHERE id=%(id)s;'
        connectToMySQL(db).query_db(query, data)

    @classmethod
    def check_email(cls, data):
        query = 'SELECT * FROM users WHERE id=%(id)s'
        user = connectToMySQL(db).query_db(query, data)

        return user[0]
