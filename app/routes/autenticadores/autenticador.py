from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.utils.decorators import role_required
from app.models import Usuario
from app import bcrypt, db

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/deletar_usuario/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def deletar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario excluido com sucesso', 'success')
    return redirect(url_for('main_bp.menu'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email   = request.form.get('email')
        senha   = request.form.get('senha')

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.senha and bcrypt.check_password_hash(usuario.senha, senha):
            login_user(usuario)
            return redirect(url_for('main_bp.menu'))
        else:
            
            flash('E-mail ou senha inválidos.', 'error')
            return redirect(url_for('auth_bp.login'))

    return render_template('main/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_bp.index'))