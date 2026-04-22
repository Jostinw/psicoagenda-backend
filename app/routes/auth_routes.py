from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import Usuario

bp_auth = Blueprint('auth', __name__)

@bp_auth.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    return redirect(url_for('auth.login'))

@bp_auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.check_password(password):
            login_user(usuario, remember=True)
            return redirect(url_for('dashboard.dashboard'))
        flash('Correo o contraseña incorrectos.', 'error')
    return render_template('login.html')

@bp_auth.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        telefono = request.form.get('telefono', '').strip()
        if Usuario.query.filter_by(email=email).first():
            flash('Este correo ya está registrado.', 'error')
            return render_template('registro.html')
        usuario = Usuario(nombre=nombre, email=email, telefono=telefono, rol='paciente')
        usuario.set_password(password)
        db.session.add(usuario)
        db.session.commit()
        login_user(usuario)
        flash('¡Cuenta creada exitosamente!', 'success')
        return redirect(url_for('dashboard.dashboard'))
    return render_template('registro.html')

@bp_auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
