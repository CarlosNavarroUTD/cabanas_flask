from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Enum

class Usuario(UserMixin, db.Model):
    __tablename__ = 'Usuario'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, unique=True, nullable=True)  # Make this nullable
    email = db.Column(db.String(254), unique=True, nullable=False)
    nombre_usuario = db.Column(db.String(255), unique=True, nullable=False)
    tipo_usuario = db.Column(Enum('cliente', 'arrendador', 'admin', name='tipo_usuario_enum'), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)  # Flask-Login uses this method


class Arrendador(db.Model):
    __tablename__ = 'Arrendador'
    id_arrendador = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuario.id'), unique=True, nullable=False)
    usuario = db.relationship('Usuario', backref=db.backref('arrendador', uselist=False), lazy=True)

class Cliente(db.Model):
    __tablename__ = 'Cliente'
    id_cliente = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuario.id'), unique=True, nullable=False)
    usuario = db.relationship('Usuario', backref=db.backref('cliente', uselist=False), lazy=True)

class Cabana(db.Model):
    __tablename__ = 'Cabana'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    capacidad = db.Column(db.Integer, nullable=False)
    costo_por_noche = db.Column(db.Float, nullable=False)
    ubicacion = db.Column(db.String(255), nullable=False)
    estado = db.Column(Enum('disponible', 'ocupada', 'mantenimiento', 'inactiva', name='cabana_estado_enum'), default='disponible')
    arrendador_id = db.Column(db.Integer, db.ForeignKey('Arrendador.id_arrendador'), nullable=False)

class Amenidad(db.Model):
    __tablename__ = 'Amenidad'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)

class CabanaAmenidad(db.Model):
    __tablename__ = 'CabanaAmenidad'
    id = db.Column(db.Integer, primary_key=True)
    cabana_id = db.Column(db.Integer, db.ForeignKey('Cabana.id'), nullable=False)
    amenidad_id = db.Column(db.Integer, db.ForeignKey('Amenidad.id'), nullable=False)
    cabana = db.relationship('Cabana', backref=db.backref('cabana_amenidades', lazy=True))
    amenidad = db.relationship('Amenidad', backref=db.backref('cabana_amenidades', lazy=True))

class Resena(db.Model):
    __tablename__ = 'Resena'
    id = db.Column(db.Integer, primary_key=True)
    cabana_id = db.Column(db.Integer, db.ForeignKey('Cabana.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuario.id_usuario'), nullable=False)
    calificacion = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    cabana = db.relationship('Cabana', backref=db.backref('resenas', lazy=True))
    usuario = db.relationship('Usuario', backref=db.backref('resenas', lazy=True))

class Actividad(db.Model):
    __tablename__ = 'Actividad'
    id = db.Column(db.Integer, primary_key=True)
    arrendador_id = db.Column(db.Integer, db.ForeignKey('Arrendador.id_arrendador'), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    costo = db.Column(db.Float, nullable=False)
    arrendador = db.relationship('Arrendador', backref=db.backref('actividades', lazy=True))

class Paquete(db.Model):
    __tablename__ = 'Paquete'
    id = db.Column(db.Integer, primary_key=True)
    arrendador_id = db.Column(db.Integer, db.ForeignKey('Arrendador.id_arrendador'), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    noches = db.Column(db.Integer)
    precio_base = db.Column(db.Float, nullable=False)
    arrendador = db.relationship('Arrendador', backref=db.backref('paquetes', lazy=True))

class PaqueteCabana(db.Model):
    __tablename__ = 'PaqueteCabana'
    id = db.Column(db.Integer, primary_key=True)
    paquete_id = db.Column(db.Integer, db.ForeignKey('Paquete.id'), nullable=False)
    cabana_id = db.Column(db.Integer, db.ForeignKey('Cabana.id'), nullable=False)
    paquete = db.relationship('Paquete', backref=db.backref('cabanas', lazy=True))
    cabana = db.relationship('Cabana', backref=db.backref('paquetes', lazy=True))

class PaqueteActividad(db.Model):
    __tablename__ = 'PaqueteActividad'
    id = db.Column(db.Integer, primary_key=True)
    paquete_id = db.Column(db.Integer, db.ForeignKey('Paquete.id'), nullable=False)
    actividad_id = db.Column(db.Integer, db.ForeignKey('Actividad.id'), nullable=False)
    paquete = db.relationship('Paquete', backref=db.backref('actividades', lazy=True))
    actividad = db.relationship('Actividad', backref=db.backref('paquetes', lazy=True))

class ImagenActividad(db.Model):
    __tablename__ = 'ImagenActividad'
    id = db.Column(db.Integer, primary_key=True)
    actividad_id = db.Column(db.Integer, db.ForeignKey('Actividad.id'), nullable=False)
    imagen = db.Column(db.String(255), nullable=False)
    es_principal = db.Column(db.Boolean, default=False)
    actividad = db.relationship('Actividad', backref=db.backref('imagenes', lazy=True, cascade='all, delete-orphan'))

class ImagenAmenidad(db.Model):
    __tablename__ = 'ImagenAmenidad'
    id = db.Column(db.Integer, primary_key=True)
    amenidad_id = db.Column(db.Integer, db.ForeignKey('Amenidad.id'), nullable=False)
    imagen = db.Column(db.String(255), nullable=False)
    amenidad = db.relationship('Amenidad', backref=db.backref('imagenes', lazy=True, cascade='all, delete-orphan'))

class ImagenCabana(db.Model):
    __tablename__ = 'ImagenCabana'
    id = db.Column(db.Integer, primary_key=True)
    cabana_id = db.Column(db.Integer, db.ForeignKey('Cabana.id'), nullable=False)
    imagen = db.Column(db.String(255), nullable=False)
    es_principal = db.Column(db.Boolean, default=False)
    cabana = db.relationship('Cabana', backref=db.backref('imagenes', lazy='dynamic', cascade='all, delete-orphan'))

