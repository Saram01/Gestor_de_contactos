from unittest.mock import MagicMock
from src.model.gestor_contactos import GestorDeContactos

def test_agregar_contacto_mockeado():
    gestor = GestorDeContactos()

    gestor.db = MagicMock()

    contacto_mock = {
        "nombre": "Prueba",
        "categoria": "Trabajo",
        "email": "prueba@example.com",
        "telefono": "1231231234",
        "usuario_id": 1
    }

    resultado = GestorDeContactos.agregar_contacto(**contacto_mock)

    assert resultado == "Contacto agregado exitosamente."

if __name__ == "__main__":
    test_agregar_contacto_mockeado()
    print("✅ Prueba ejecutada con mock correctamente.")