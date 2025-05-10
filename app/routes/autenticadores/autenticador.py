from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from flask_login import current_user, login_user, logout_user
from app.models import Usuario
from app import bcrypt

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = Usuario.query.filter_by(email=request.form.get('email')).first()
        session['user_id'] = usuario.id

        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.senha and bcrypt.check_password_hash(usuario.senha, senha):
            login_user(usuario)
            return redirect(url_for('main_bp.menu'))
        else:

            flash('E-mail ou senha inválidos.', 'error')
            return redirect(url_for('auth_bp.login'))

    global usuario_logado
    usuario_logado = current_user.is_authenticated
    return render_template('main/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('main_bp.index'))
