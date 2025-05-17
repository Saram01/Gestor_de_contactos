from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import declarative_base
#from sqlalchemy import inspect




url_conexion = "postgresql://mamau:postgres@localhost:5432/Contactos"

engine = create_engine(url_conexion, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String(30), unique=True, nullable=False)
    contrasena = Column(String(100), nullable=False)
    contactos = relationship("Contacto", back_populates="usuario")

    def __repr__(self):
        return f"<Usuario(nombre_usuario={self.nombre_usuario})>"

class Contacto(Base):
    __tablename__ = 'contacto'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    categoria = Column(String(30))
    email = Column(String(100), unique=True)
    telefono = Column(String(20), unique=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    usuario = relationship("Usuario", back_populates="contactos")

    def __repr__(self):
        return f"<Contacto(nombre={self.nombre}, categoria={self.categoria})>"

Base.metadata.create_all(bind=engine)

#inspector = inspect(engine)
#print(inspector.get_table_names())
