from flask import render_template, jsonify, request
from src.model.gestor_contactos import GestorDeContactos
from src.model.contactos import Contacto
from src.model.excepciones import ContactError, InvalidEmailError, InvalidPhoneNumberError

gestor = GestorDeContactos()

def register_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/contactos', methods=['GET'])
    def obtener_contactos():
        contactos = gestor.listar_contactos()
        return jsonify([c.to_dict() for c in contactos])

    @app.route('/api/contactos', methods=['POST'])
    def agregar_contacto():
        data = request.get_json()
        try:
            contacto = Contacto(
                nombre=data['nombre'],
                telefono=data['telefono'],
                email=data['email'],
                categoria=data['categoria']
            )
            gestor.agregar_contacto(contacto)
            return jsonify({'mensaje': 'Contacto agregado exitosamente'}), 201
        except (ContactError, InvalidEmailError, InvalidPhoneNumberError) as e:
            return jsonify({'error': str(e)}), 400
