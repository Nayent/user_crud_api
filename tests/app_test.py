import unittest
from app import create_app, db
from app.models import Usuario

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
        self.client = self.app.test_client()
        self.token = 'TesteToken123'

        with self.app.app_context():
            db.create_all()
            user = Usuario(name='user_test', description='Test Description')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_users_with_token(self):
        response = self.client.get('/users', query_string={"token": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('users', response.json)

    def test_get_users_without_token(self):
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {'message': 'Token inválido ou ausente!'})
    
    def test_get_users_with_invalid_token(self):
        invalid_token = 'invalid_token'
        response = self.client.get('/users', query_string={"token": invalid_token})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {'message': 'Token inválido ou ausente!'})

    def test_get_user_by_id(self):
        response = self.client.get('/users/1', query_string={"token": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.json)

    def test_create_user_with_json(self):
        user_data = {
            'name': 'user1',
            'description': 'This is user1'
        }
        response = self.client.post('/users', json=user_data, query_string={"token": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['user']['name'], 'user1')
        self.assertEqual(response.json['user']['description'], 'This is user1')

    def test_create_user_without_json(self):
        user_data = {}
        response = self.client.post('/users', json=user_data, query_string={"token": self.token})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'message': 'Body incompleto! O campo name é obrigatório!'})

    def test_update_user(self):
        new_user_data = {
            'name': 'user10',
            'description': 'This is not user1'
        }
        response = self.client.put('/users/1', json=new_user_data, query_string={"token": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['user']['name'], 'user10')
        self.assertEqual(response.json['user']['description'], 'This is not user1')
    
    def test_delete_user(self):
        response = self.client.delete('/users/1', query_string={"token": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Usuário excluído com sucesso!'})
    
    def test_delete_non_existent_user(self):
        response = self.client.delete('/users/999999', query_string={"token": self.token})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'message': 'Usuário não encontrado!'})

if __name__ == '__main__':
    unittest.main()
