import os
import sys
from models import User

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from flask_restful import reqparse, abort, Resource, fields, marshal_with

parser_user = reqparse.RequestParser()
parser_user.add_argument('first_name')
parser_user.add_argument('last_name')
parser_user.add_argument('birthdate')
parser_user.add_argument('email')
parser_user.add_argument('password')
parser_user.add_argument('type')
parser_user.add_argument('rating')

user_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'birthdate': fields.DateTime(dt_format='iso8601'),
    'email': fields.String,
    'password': fields.String,
    'type': fields.String,
    'rating': fields.Float
}

class Database(object):
    def get_session(self):
        """Return new session
        Returns:
            [Session] -- [Return a new session]
        """
        connection = os.environ.get("DATABASE_URL")
        engine = create_engine(connection)
        connection = engine.connect()
        Session = sessionmaker(bind=engine)        
        session = Session()
        return session

    def findAllUsers(self):
        session = self.get_session()
        users = session.query(User)

        session.close()
        return [u.serialize() for u in users]

    def findUserById(self, user_id):
        session = self.get_session()
        user = session.query(User).filter_by(id = user_id).first()
        session.close()
        print(f"\n\n{user}\n\n", file=sys.stderr)
        if (user):
            return user.serialize()
        else:
            abort(404, error=f'User with id {user_id} not found')

        return False

    def saveUser(self, u):
        """Creates a new user
    
        Returns:
            [id of created user]
        """
        session = self.get_session()
        user = User(
            first_name=u.first_name,
            last_name=u.last_name,
            birthdate = u.birthdate,
            email = u.email,
            password = u.password,
            _type = u._type,
            rating = u.rating 
            )
        session.add(user)
        session.commit()
        session.close()
        print(f'\n\n\n{user.serialize()}', file=sys.stderr)     
        return user.serialize()

class UserListAPI(Resource):
    @marshal_with(user_fields)
    def get(self):
        db_api = Database()
        users = db_api.findAllUsers()
        return users

    @marshal_with(user_fields)
    def post(self):
        db_api = Database()
        args = parser_user.parse_args()
        user = User(
            first_name=args['first_name'],
            last_name=args['last_name'],
            birthdate=args['birthdate'],
            email=args['email'],
            password=args['password'],
            _type=args['type'],
            rating=args['rating']
            )
        return db_api.saveUser(user)


class UserAPI(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        db_api = Database()
        user = db_api.findUserById(user_id)
        return user