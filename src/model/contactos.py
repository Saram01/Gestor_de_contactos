class Contacto:
    def __init__(self, nombre: str, email: str, telefono: int, categoria: str):
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.categoria = categoria
    
    def __str__(self):
        return f"{self.nombre} ({self.categoria}): {self.email}, {self.telefono}"
