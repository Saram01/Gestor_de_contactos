from flask import Flask, render_template, request, redirect, url_for
from src.model.gestor_contactos import GestorDeContactos
from src.model.contactos import Contacto
from src.model.excepciones import *

app = Flask(__name__)
gestor = GestorDeContactos()

@app.route('/')
def index():
    contactos = gestor.listar_contactos()
    return render_template('index.html', contactos=contactos)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            telefono = request.form['telefono']
            email = request.form['email']
            categoria = request.form['categoria']
            contacto = Contacto(nombre, telefono, email, categoria)
            gestor.agregar_contacto(contacto)
            return redirect(url_for('index'))
        except ContactError as e:
            return f"Error: {e}"
    return render_template('agregar.html')

@app.route('/editar/<nombre>', methods=['GET', 'POST'])
def editar(nombre):
    contacto = gestor.buscar_contacto(nombre)
    if request.method == 'POST':
        try:
            telefono = request.form['telefono']
            email = request.form['email']
            categoria = request.form['categoria']
            gestor.editar_contacto(nombre, telefono=telefono, email=email, categoria=categoria)
            return redirect(url_for('index'))
        except ContactError as e:
            return f"Error: {e}"
    return render_template('editar.html', contacto=contacto)

@app.route('/eliminar/<nombre>')
def eliminar(nombre):
    try:
        gestor.eliminar_contacto(nombre)
        return redirect(url_for('index'))
    except ContactError as e:
        return f"Error: {e}"

@app.route('/buscar', methods=['GET'])
def buscar():
    categoria = request.args.get('categoria', '')
    contactos = gestor.filtrar_contacto(categoria)
    return render_template('index.html', contactos=contactos)
