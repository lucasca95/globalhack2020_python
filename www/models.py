import os
from flask_restful import reqparse, abort, Resource, fields, marshal_with
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

parser = reqparse.RequestParser()
parser.add_argument('first_name')
parser.add_argument('last_name')
parser.add_argument('email')
parser.add_argument('password')
parser.add_argument('type')

user_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'password': fields.String,
    'type': fields.String
}
delete_message = {
    'message': fields.String
}

class UserDao(object):
    def __init__(self, id, first_name, last_name, email, password, _type):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.type = _type

        # This field will not be sent in the response
        self.status = 'active'
    
    
    def findAllUsers():
        users = db.execute('SELECT id, first_name, last_name, email, type FROM appuser').fetchall()
        users_list = []
        for u in users:
            users_list.append(
                {'id': u.id,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'email': u.email,
                'password': 'TOP_SECRET',
                'type': u.type})
                # UserDao(u.id, u.first_name, u.last_name, u.email, u.password, u.type))
        return users_list
    
    def findUserById(user_id):
        user = db.execute('SELECT id, first_name, last_name, email, type \
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
        db.execute('INSERT INTO appuser (first_name, last_name, email, password, type) \
            VALUES(:first_name, :last_name, :email, :password, :type)',
            {'first_name': u.first_name, 'last_name': u.last_name, 'email': u.email, 'password': u.password, 'type': u.type})
        try:
            db.commit()
        except:
            abort(404, error=f'Error when saving user to DB')

        return {'id': u.id,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'email': u.email,
                'type': u.type}

class User(Resource):

    @marshal_with(user_fields)
    def get(self, user_id):
        return UserDao.findUserById(user_id)
    
    @marshal_with(delete_message)
    def delete(self, user_id):
        UserDao.deleteUserById(user_id)
        return {'message': 'User Deleted'}
    
    
    def put(self, todo_id):
        args = parser.parse_args()
        print(f'\n\n{args}\n\n')
        return "testeando el put"


class UserList(Resource):
    @marshal_with(user_fields)
    def get(self):
        return UserDao.findAllUsers()

    @marshal_with(user_fields)
    def post(self):
        args = parser.parse_args()
        u = UserDao(0,args['first_name'], args['last_name'], args['email'], args['password'], args['type'])
        return UserDao.saveUser(u), 200