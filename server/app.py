#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User, UserSchema

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204



class Signup(Resource):

    def post(self):

        data = request.get_json()

        new_user = User(username=data['username'])
        new_user.password_hash = data['password']

        db.session.add(new_user)
        db.session.commit()

        user_schema = UserSchema()
        user_dict = user_schema.dump(new_user)

        session['user_id'] = new_user.id

        return user_dict, 201



class CheckSession(Resource):

    def get(self):

        if session.get('user_id'):
            user = User.query.filter_by(id=session['user_id']).first()
            user_schema = UserSchema()
            user_dict = user_schema.dump(user)

            return user_dict, 200

        else:
            return {}, 204



class Login(Resource):

    def post(self):

        data = request.get_json()

        user = User.query.filter_by(username=data['username']).first()

        if user and user.authenticate(data['password']):
            session['user_id'] = user.id
            user_schema = UserSchema()
            user_dict = user_schema.dump(user)

            return user_dict, 200

        else:
            return {}, 401



class Logout(Resource):

    def delete(self):

        session['user_id'] = None

        return {}, 204

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
