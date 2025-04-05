from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.utils.decorators import role_required
from app.models import Usuario
from app import bcrypt, db

adm_bp = Blueprint('adm_bp', __name__)

@adm_bp.route('/registro', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def registro():
    if request.method == 'POST':
        nome    = request.form.get('name')
        email   = request.form.get('email')
        senha   = request.form.get('senha')
        role    = request.form.get('role')

        verificar_email = Usuario.query.filter_by(email=email).first()
        if verificar_email:
            flash('Email já cadastrado', 'error')
            return redirect(url_for('adm_bp.usuarios'))

        senha_criptografada = bcrypt.generate_password_hash(senha).decode('utf-8')
        usuario = Usuario(nome=nome, email=email, senha=senha_criptografada, role=role)
        db.session.add(usuario)
        db.session.commit()
        flash('Registro realizado com sucesso!', 'success')
        return redirect(url_for('adm_bp.usuarios'))

    return render_template('usuarios/registrar_usuario.html')

@adm_bp.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    if request.method == 'POST':
        usuario.nome = request.form.get('name')
        usuario.email = request.form.get('email')
        usuario.senha = bcrypt.generate_password_hash(request.form.get('senha')).decode('utf-8')
        usuario.role = request.form.get('role')

        db.session.commit()
        flash('Usuario editado com sucesso', 'success')
        return redirect(url_for('main_bp.menu'))
    return render_template('usuarios/editar_usuario.html', usuario=usuario)
