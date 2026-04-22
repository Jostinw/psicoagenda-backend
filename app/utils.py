from datetime import date
from app.models import Usuario, Cita
from app.extensions import db

def crear_datos_demo():
    if not Usuario.query.first():
        admin = Usuario(nombre='Dr. Carlos Martínez', email='admin@psico.com', rol='admin', telefono='099-000-0001')
        admin.set_password('admin123')
        p1 = Usuario(nombre='Ana Mora', email='ana@demo.com', rol='paciente', telefono='099-000-0002')
        p1.set_password('paciente123')
        p2 = Usuario(nombre='Luis Peña', email='luis@demo.com', rol='paciente', telefono='099-000-0003')
        p2.set_password('paciente123')
        db.session.add_all([admin, p1, p2])
        db.session.commit()
        hoy = date.today()
        c1 = Cita(paciente_id=p1.id, psicologo_id=admin.id, fecha=hoy, hora='09:00', tipo='Sesión inicial', estado='confirmada')
        c2 = Cita(paciente_id=p2.id, psicologo_id=admin.id, fecha=hoy, hora='11:00', tipo='Seguimiento', estado='pendiente')
        db.session.add_all([c1, c2])
        db.session.commit()
        print("Datos de demo creados con éxito.")
        print("   Admin: admin@psico.com / admin123")
        print("   Paciente: ana@demo.com / paciente123")
