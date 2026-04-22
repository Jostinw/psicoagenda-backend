from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app.extensions import db

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    rol = db.Column(db.String(20), default='paciente')  # 'admin' o 'paciente'
    telefono = db.Column(db.String(20))
    creado = db.Column(db.DateTime, default=datetime.utcnow)
    citas_paciente = db.relationship('Cita', foreign_keys='Cita.paciente_id', backref='paciente', lazy=True)
    citas_psicologo = db.relationship('Cita', foreign_keys='Cita.psicologo_id', backref='psicologo', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Cita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    psicologo_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.String(10), nullable=False)
    tipo = db.Column(db.String(50), default='Sesión individual')
    estado = db.Column(db.String(20), default='pendiente')  # pendiente, confirmada, cancelada, completada
    notas = db.Column(db.Text)
    creada = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'paciente': self.paciente.nombre,
            'psicologo': self.psicologo.nombre,
            'fecha': self.fecha.strftime('%Y-%m-%d'),
            'hora': self.hora,
            'tipo': self.tipo,
            'estado': self.estado,
            'notas': self.notas or ''
        }
