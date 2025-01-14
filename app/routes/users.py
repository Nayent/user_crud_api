from flask import Blueprint, request, jsonify
from app.models import Usuario
from app.auth import token_required
from app import db

users_bp = Blueprint('users', __name__)

# Create user
@users_bp.route('/users', methods=['POST'])
@token_required
def create_user():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({"message": "Body incompleto! O campo name é obrigatório!"}), 400
    new_user = Usuario(name=data['name'], description=data.get('description', ''))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        "message": "Usuário criado com sucesso!",
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

    users_query = Usuario.query.paginate(page=page, per_page=per_page, error_out=False)
    
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
    user = Usuario.query.get(user_id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado!'}), 404
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
    user = Usuario.query.get(user_id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado!'}), 404
    user.name = data.get('name', user.name)
    user.description = data.get('description', user.description)

    db.session.commit()
    return jsonify({
        "message": "Usuário atualizado com sucesso!",
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
    user = Usuario.query.get(user_id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado!'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Usuário excluído com sucesso!"})
