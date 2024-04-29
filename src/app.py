
import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger
from api.utils import APIException, generate_sitemap
from api.models import db, Trainer, Trainer_data, User, User_data
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager


from datetime import timedelta

# from models import Person

ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '../public/')
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'
jwt = JWTManager(app)
# database condiguration
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db, compare_type=True)
db.init_app(app)
# add the admin
setup_admin(app)

# add the admin
setup_commands(app)

# Add all endpoints form the API with a "api" prefix
app.register_blueprint(api, url_prefix='/api')

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    if ENV == "development":
        return generate_sitemap(app)
    return send_from_directory(static_file_dir, 'index.html')

# any other endpoint will try to serve it like a static file


@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0  # avoid cache memory
    return response


@app.route('/login', methods=['POST'])
def login (): 
    data =request.json
    if not data:
        APIException("Insert correct information"), 400

    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        APIException("Missing email or password"), 400

    user = User.query.filter_by(email=email).first()
    trainer = Trainer.query.filter_by(email=email).first()

    if (user and password != user.password) or (trainer and password != trainer.password):
        APIException("Invalid password, please try again"), 401
    
    access_token = create_access_token(identity=email)
   
    return jsonify({ "access_token": access_token}), 200
    

@app.route('/signup', methods=['POST'])
def create_new_user ():
    data = request.json
    check_if_email_already_exists = User.query.filter_by(email = data["email"]).first()
    if check_if_email_already_exists:
        APIException("Email already exists")
    
    new_user = User(
        user_name= data["user_name"], 
        email= data["email"],
        password= data["password"],
        role = "user",
    )

    db.session.add(new_user)
    db.session.commit()
    serialized_new_user = new_user.serialize()

    return jsonify(serialized_new_user), 200

@app.route('/trainer/<int:id>')
def get_trainer_users (id):
    trainer = Trainer_data.query.filter_by(trainer_data_id=id).first()
    if not trainer:
        APIException('User not found')
    
    users = User_data.query.get_all(trainer_id=id)
    serialized_users = (user.serialize () for user in users)
    
    return jsonify(serialized_users), 200
    
@app.route('/trainer/<int:trainer_id>/<int:user_id>')
def get_single_user_from_trainer (trainer_id, user_id):
    get_particular_user = User_data.query.filter_by(trainer_id=trainer_id, user_id = user_id)

    if not get_particular_user:
        APIException("Not users associated with this account"), 400
    serialized_user = get_particular_user.serialize()

    return jsonify(serialized_user), 200






# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)

