from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Configurar la conexión a la base de datos PostgreSQL
DATABASE_URL = "postgresql://mamau:@localhost:5432/Contactos"

# Crear un motor de base de datos (engine)
engine = create_engine(DATABASE_URL, echo=True)

# Crear una clase base para las definiciones de nuestras tablas
Base = declarative_base()

# Definir la clase Usuario
class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String(30), unique=True, nullable=False)
    contrasena = Column(String(100), nullable=False)

    # Relación con la tabla contacto
    contactos = relationship("Contacto", back_populates="usuario")

    def __repr__(self):
        return f"<Usuario(nombre_usuario={self.nombre_usuario})>"

# Definir la clase Contacto
class Contacto(Base):
    __tablename__ = 'contacto'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    categoria = Column(String(30))
    email = Column(String(100), unique=True)
    telefono = Column(String(20), unique=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)

    # Relación con la tabla usuario
    usuario = relationship("Usuario", back_populates="contactos")

    def __repr__(self):
        return f"<Contacto(nombre={self.nombre}, categoria={self.categoria})>"

# Crear la sesión (session)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)
