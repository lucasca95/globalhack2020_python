
from database import Database, UserListAPI, UserAPI
from flask import Flask
# from models import User
import os
from flask_restful import Api


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

db = Database()

api = Api(app)
api.add_resource(UserListAPI,'/users/')
api.add_resource(UserAPI,'/users/<int:user_id>')


###############################################################
@app.route('/', methods=['GET'])
def welcome():
    return "SERVER RUNNING"
###############################################################

if __name__ == '__main__':
    app.run(host='0.0.0.0')























# ###############################################################
# @app.route("/api/users", methods=["GET"])
# def findAllUsers():
#     users = db.execute('SELECT id, first_name, last_name, birthdate, email, type FROM appuser').fetchall()
#     users_list = []
#     for u in users:
#         users_list.append(
#             {
#                 'first_name': u.first_name,
#                 'last_name': u.last_name,
#                 'birthdate': u.birthdate,
#                 'email': u.email,
#                 'type': u.type,
#                 'id': u.id
#             })
#     return jsonify(users_list)
# ###############################################################

# ###############################################################
# @app.route("/api/petitions", methods=["GET"])
# def findAllPetitions():
#     petitions = db.execute('SELECT id, day, hour, helped_id, collaborator_id FROM petition').fetchall()
#     petitions_list = []
#     for p in petitions:

#         u_collaborator = getUserById(p.collaborator_id)
#         u_helped = getUserById(p.helped_id)

#         petitions_list.append(
#             {
#                 'id': p.id,
#                 'day': p.day,
#                 'hour': p.hour,
#                 'collaborator': {
#                     'first_name': u_collaborator.first_name,
#                     'last_name': u_collaborator.last_name,
#                     'id': u_collaborator.id,
#                     'birthdate': u_collaborator.birthdate,
#                     'email': u_collaborator.email,
#                     'type': u_collaborator.type
#                 },
#                 'helped': {
#                     'first_name': u_helped.first_name,
#                     'last_name': u_helped.last_name,
#                     'id': u_helped.id,
#                     'birthdate': u_helped.birthdate,
#                     'email': u_helped.email,
#                     'type': u_helped.type
#                 }
#             })
#     return jsonify(petitions_list)
# ###############################################################

# ###############################################################
# @app.route("/api/reviews", methods=["GET"])
# def findAllReviews():
#     reviews = db.execute('SELECT id, day, hour, helped_id, collaborator_id FROM petition').fetchall()
    
#     return "Get reviews"
# ###############################################################


# @app.route("/login", methods=["GET","POST"])
# def login():
#     return render_template("error.html", message="Access violation error.")

# @app.route("/logout")
# def logout():
#     return "logout page"

# @app.route("/register/", methods=["GET", "POST"])
# def register():
#     return "register page"


# #####################################################
# #####               Métos extra                 #####
# #####################################################

# def getUserById(user_id):
#     user = db.execute('SELECT id, first_name, last_name, birthdate, email, type \
#         FROM appuser \
#         WHERE id = :user_id',
#         {'user_id': user_id}).fetchone()
#     return user