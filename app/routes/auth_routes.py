from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Usuario
from flask_login import login_user, logout_user, login_required
from app import bcrypt
from app import db
from app.utils.decorators import role_required

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/registro', methods=['GET', 'POST'])
@role_required('admin')
def registro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        role = request.form.get('role')

        verificar_email = Usuario.query.filter_by(email=email).first()
        if verificar_email:
            flash('Email já cadastrado', 'error')
            return redirect(url_for('auth_bp.registro'))

        senha_criptografada = bcrypt.generate_password_hash(senha).decode('utf-8')
        usuario = Usuario(nome=nome, email=email, senha=senha_criptografada, role=role)
        db.session.add(usuario)
        db.session.commit()
        flash('Registro realizado com sucesso!', 'success')
        return redirect(url_for('auth_bp.login'))

    return render_template('main/registro.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        # Verificar se o usuário existe
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.senha and bcrypt.check_password_hash(usuario.senha, senha):
            login_user(usuario)
            return redirect(url_for('main_bp.menu'))
        else:
            # Redirecionar de volta ao login em caso de erro
            flash('E-mail ou senha inválidos.', 'error')
            return redirect(url_for('auth_bp.login'))

    return render_template('main/login.html')

@auth_bp.route('/logout')
@role_required('user', 'supervisor', 'admin')
@login_required
def logout():
    logout_user()
    flash('Você deslogou do sistema','info')
    return redirect(url_for('main_bp.index'))