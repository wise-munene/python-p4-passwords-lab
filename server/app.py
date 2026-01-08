#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        user = User(
            username=json['username'] 
        )
        user.password_hash = json['password']
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id') # Get user_id from session
        if user_id:
            user =User.query.get(user_id) # Query the User model
            return user.to_dict(), 200
        else:
            return {}, 204 # No content if no user_id in session


class Login(Resource):
    def post(self):
        data = request.get_json() 
        user = User.query.filter_by(username=data['username']).first() # Query User by username
        if user and user.authenticate(data['password']): # Check password
            session['user_id'] = user.id # Set user_id in session
            return user.to_dict(), 200
        else:
            return {'error': 'Invalid credentials'}, 401


class Logout(Resource):
    def delete(self):
        session['user_id'] = None # Clear user_id from session
        return {}, 204

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
