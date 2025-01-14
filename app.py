from app import create_app, db
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'TesteToken123'

db.init_app(app)

from app.routes.users import users_bp
app.register_blueprint(users_bp)

@app.route('/test')
def test_route():
    return jsonify({"message": "Test route is working!"})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
