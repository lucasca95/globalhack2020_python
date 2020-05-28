import os
import datetime
from flask_restful import reqparse, abort, Resource, fields, marshal_with
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

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
delete_message = {
    'message': fields.String
}

class UserDao(object):
    def __init__(self, id=None, first_name=None, last_name=None, birthdate=None, email=None, password=None, _type=None, rating=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.email = email
        self.password = password
        self.type = _type
        self.rating = rating

        # This field will not be sent in the response
        self.status = 'active'
    
    def findAllUsers():
        users = db.execute('SELECT id, first_name, last_name, birthdate, email, type, rating FROM appuser').fetchall()
        users_list = []
        for u in users:
            # print(f'\n{type(u.birthdate)}\n')
            users_list.append(
                UserDao(u.id, u.first_name, u.last_name, u.birthdate, u.email, 'TOP SECRET', u.type, u.rating))
                # {'id': u.id,
                # 'first_name': u.first_name,
                # 'last_name': u.last_name,
                # 'email': u.email,
                # 'password': 'TOP_SECRET',
                # 'type': u.type})
        return users_list
    
    def findUserById(user_id):
        user = db.execute('SELECT id, first_name, last_name, birthdate, email, type, rating  \
        FROM appuser \
        WHERE id = :user_id',
        {'user_id': user_id}).fetchone()
        if (user):
            return user
        else:
            abort(404, error=f'User with id {user_id} not found')
        return None
    
    def deleteUserById(user_id):
        u = UserDao.findUserById(user_id)
        db.execute('DELETE \
            FROM appuser \
            WHERE id = :user_id',
            {'user_id': user_id})
        try:
            db.commit()
        except:
            abort(404, error=f'Error when deleting user with id = {user_id}')
        return True

    def saveUser(u):
        db.execute('INSERT INTO appuser (first_name, last_name, birthdate, email, password, type, rating) \
            VALUES(:first_name, :last_name, :birthdate, :email, :password, :type, :rating)',
            {'first_name': u.first_name, 'last_name': u.last_name, 'birthdate': u.birthdate,
            'email': u.email, 'password': u.password, 'type': u.type, 'rating': u.rating})
        try:
            db.commit()
        except:
            abort(404, error=f'Error when saving user to DB')

        return u

class User(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        return UserDao.findUserById(user_id)
    
    @marshal_with(delete_message)
    def delete(self, user_id):
        UserDao.deleteUserById(user_id)
        return {'message': 'User Deleted'}
    
    def put(self, todo_id):
        args = parser_user.parse_args()
        print(f'\n\n{args}\n\n')
        return "testeando el put"


class UserList(Resource):
    @marshal_with(user_fields)
    def get(self):
        return UserDao.findAllUsers()

    @marshal_with(user_fields)
    def post(self):
        args = parser_user.parse_args()
        u = UserDao(0,
            args['first_name'], 
            args['last_name'], 
            args['birthdate'], 
            args['email'], 
            args['password'], 
            args['type'],
            args['rating'], 
        )
        return UserDao.saveUser(u), 200