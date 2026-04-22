from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Usuario

bp_pacientes = Blueprint('pacientes', __name__)

@bp_pacientes.route('/pacientes')
@login_required
def pacientes():
    if current_user.rol != 'admin':
        return redirect(url_for('dashboard.dashboard'))
    lista = Usuario.query.filter_by(rol='paciente').order_by(Usuario.nombre).all()
    return render_template('pacientes.html', pacientes=lista)
