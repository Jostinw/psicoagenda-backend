from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from app.extensions import db
from app.models import Usuario, Cita

bp_citas = Blueprint('citas', __name__)

@bp_citas.route('/citas')
@login_required
def citas():
    if current_user.rol != 'admin':
        return redirect(url_for('dashboard.dashboard'))
    todas = Cita.query.order_by(Cita.fecha.desc(), Cita.hora).all()
    psicologos = Usuario.query.filter_by(rol='admin').all()
    pacientes = Usuario.query.filter_by(rol='paciente').all()
    return render_template('citas.html', citas=todas, psicologos=psicologos, pacientes=pacientes)

@bp_citas.route('/citas/nueva', methods=['POST'])
@login_required
def nueva_cita():
    if current_user.rol == 'admin':
        paciente_id = request.form.get('paciente_id')
        psicologo_id = current_user.id
    else:
        paciente_id = current_user.id
        psicologo_id = request.form.get('psicologo_id')
        if not psicologo_id:
            primer_admin = Usuario.query.filter_by(rol='admin').first()
            psicologo_id = primer_admin.id if primer_admin else 1

    fecha_str = request.form.get('fecha')
    hora = request.form.get('hora')
    tipo = request.form.get('tipo', 'Sesión individual')
    notas = request.form.get('notas', '')

    if not paciente_id:
        flash('Debe seleccionar un paciente válido.', 'error')
        return redirect(request.referrer or url_for('dashboard.dashboard'))

    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except ValueError:
        flash('Fecha inválida.', 'error')
        return redirect(request.referrer or url_for('dashboard.dashboard'))

    from datetime import date
    hoy = date.today()
    if current_user.rol != 'admin' and fecha < hoy:
        flash('No puedes agendar citas en fechas pasadas.', 'error')
        return redirect(request.referrer or url_for('dashboard.dashboard'))

    # Validar si el psicólogo seleccionado ya tiene una cita ocupada en esa fecha y hora
    cita_psicologo = Cita.query.filter_by(
        psicologo_id=psicologo_id,
        fecha=fecha,
        hora=hora
    ).filter(Cita.estado != 'cancelada').first()

    if cita_psicologo:
        flash('El psicólogo ya tiene una cita agendada en esa fecha y hora.', 'error')
        return redirect(request.referrer or url_for('dashboard.dashboard'))

    # Validar si el paciente ya tiene otra cita agendada en esa fecha y hora
    cita_paciente = Cita.query.filter_by(
        paciente_id=paciente_id,
        fecha=fecha,
        hora=hora
    ).filter(Cita.estado != 'cancelada').first()

    if cita_paciente:
        if current_user.rol == 'admin':
            flash('El paciente seleccionado ya tiene una cita agendada en esa fecha y hora.', 'error')
        else:
            flash('Ya tienes una cita agendada en esa fecha y hora.', 'error')
        return redirect(request.referrer or url_for('dashboard.dashboard'))

    cita = Cita(paciente_id=paciente_id, psicologo_id=psicologo_id,
                fecha=fecha, hora=hora, tipo=tipo, notas=notas)
    db.session.add(cita)
    db.session.commit()
    flash('Cita agendada exitosamente.', 'success')
    return redirect(url_for('dashboard.dashboard'))

@bp_citas.route('/citas/<int:cita_id>/estado', methods=['POST'])
@login_required
def cambiar_estado(cita_id):
    if current_user.rol != 'admin':
        return jsonify({'error': 'Sin permiso'}), 403
    cita = Cita.query.get_or_404(cita_id)
    nuevo_estado = request.form.get('estado')
    if nuevo_estado in ['pendiente', 'confirmada', 'cancelada', 'completada']:
        cita.estado = nuevo_estado
        db.session.commit()
        flash(f'Estado actualizado a "{nuevo_estado}".', 'success')
    return redirect(request.referrer or url_for('citas.citas'))

@bp_citas.route('/citas/<int:cita_id>/eliminar', methods=['POST'])
@login_required
def eliminar_cita(cita_id):
    if current_user.rol != 'admin':
        return jsonify({'error': 'Sin permiso'}), 403
    cita = Cita.query.get_or_404(cita_id)
    db.session.delete(cita)
    db.session.commit()
    flash('Cita eliminada.', 'success')
    return redirect(request.referrer or url_for('citas.citas'))

@bp_citas.route('/api/citas')
@login_required
def api_citas():
    if current_user.rol == 'admin':
        citas_lista = Cita.query.all()
    else:
        citas_lista = Cita.query.filter_by(paciente_id=current_user.id).all()
    return jsonify([c.to_dict() for c in citas_lista])
