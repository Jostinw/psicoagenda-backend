from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import date
from sqlalchemy import extract
from app.extensions import db
from app.models import Usuario, Cita

bp_dashboard = Blueprint('dashboard', __name__)

@bp_dashboard.route('/dashboard')
@login_required
def dashboard():
    hoy = date.today()
    if current_user.rol == 'admin':
        citas_hoy = Cita.query.filter_by(fecha=hoy).order_by(Cita.hora).all()
        total_mes = Cita.query.filter(
            extract('month', Cita.fecha) == hoy.month,
            extract('year', Cita.fecha) == hoy.year
        ).count()
        pacientes = Usuario.query.filter_by(rol='paciente').count()
        pacientes_lista = Usuario.query.filter_by(rol='paciente').order_by(Usuario.nombre).all()
        pendientes = Cita.query.filter_by(estado='pendiente').count()
        return render_template('dashboard_admin.html',
            citas_hoy=citas_hoy, total_mes=total_mes,
            pacientes=pacientes, pacientes_lista=pacientes_lista,
            pendientes=pendientes, hoy=hoy)
    else:
        mis_citas = Cita.query.filter_by(paciente_id=current_user.id)\
            .filter(Cita.fecha >= hoy).order_by(Cita.fecha, Cita.hora).all()
        return render_template('dashboard_paciente.html', citas=mis_citas, hoy=hoy)
