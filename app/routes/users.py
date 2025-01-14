from flask import Blueprint, request, jsonify
from app.models import User
from app.auth import token_required
from app import db

users_bp = Blueprint('users', __name__)

# Create user
@users_bp.route('/users', methods=['POST'])
@token_required
def create_user():
    data = request.get_json()
    new_user = User(name=data['name'], description=data.get('description', ''))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        "message": "User criado com sucesso!",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "description": new_user.description
        }
    })

# Get all users
@users_bp.route('/users', methods=['GET'])
@token_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    if per_page > 100:
        per_page = 100

    users_query = User.query.paginate(page=page, per_page=per_page, error_out=False)
    
    users = [{
        "id": user.id,
        "name": user.name,
        "description": user.description
    } for user in users_query.items]

    return jsonify({
        "users": users,
        "total": users_query.total,
        "pages": users_query.pages,
        "current_page": users_query.page,
        "per_page": users_query.per_page
    })


# Get single user
@users_bp.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        "id": user.id,
        "name": user.name,
        "description": user.description
    })

# Update user
@users_bp.route('/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    data = request.get_json()
    user = User.query.get_or_404(user_id)

    user.name = data.get('name', user.name)
    user.description = data.get('description', user.description)

    db.session.commit()
    return jsonify({
        "message": "User atualizado com sucesso!",
        "user": {
            "id": user.id,
            "name": user.name,
            "description": user.description
        }
    })

# Delete user
@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User excluído com sucesso!"})
