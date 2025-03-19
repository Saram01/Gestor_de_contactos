class Contacto:
    def __init__(self, nombre: str, email: str, telefono: int, categoria: str):
        if not self.validate_phone(telefono):
            raise ValueError("Número de teléfono inválido, debe tener al menos 10 dígitos.")
        if not self.validate_email(email):
            raise ValueError("Formato de correo electrónico inválido.")
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.categoria = categoria
    
    def __str__(self):
        return f"{self.nombre} ({self.categoria}): {self.email}, {self.telefono}"

    @staticmethod
    def validate_phone(telefono: int) -> bool:
        return len(str(telefono)) >= 10 and str(telefono).isdigit()

    @staticmethod
    def validate_email(email: str) -> bool:
        import re
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None
