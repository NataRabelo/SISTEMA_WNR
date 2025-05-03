from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from app.utils.decorators import role_required
from flask_login import login_required
from app.models import Usuario
from app import bcrypt, db

adm_bp = Blueprint('adm_bp', __name__)

@adm_bp.route('/administracao', methods=['GET'])
@login_required
@role_required('admin')
def administracao():
    return render_template('administracao/menu.html')

@adm_bp.route('/servicos', methods=['GET'])
@login_required
@role_required('admin')
def servicos():
    return render_template('administracao/menu_servicos.html')

@adm_bp.route('/usuarios', methods=['GET'])
@login_required
@role_required('admin')
def usuarios():
    return render_template('administracao/usuarios.html')

@adm_bp.route('/cadastrar_usuario', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def cadastrar_usuario():
    if request.method == 'POST':
        nome = request.form.get('name')
        email = request.form.get('email')
        senha = request.form.get('senha')
        role = request.form.get('role')

        verificar_email = Usuario.query.filter_by(email=email).first()
        if verificar_email:
            flash('Email já cadastrado', 'error')
            return redirect(url_for('adm_bp.usuarios'))

        senha_cript = bcrypt.generate_password_hash(senha).decode('utf-8')
        usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha_cript,
            role=role
        )
        db.session.add(usuario)
        db.session.commit()
        flash('Registro realizado com sucesso!', 'success')
        return redirect(url_for('adm_bp.usuarios'))

    return render_template('administracao/form.html')

@adm_bp.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':
        usuario.nome = request.form.get('name')
        usuario.email = request.form.get('email')
        nova_senha = request.form.get('senha')

        if nova_senha:
            usuario.senha = bcrypt.generate_password_hash(nova_senha).decode('utf-8')

        usuario.role = request.form.get('role')
        db.session.commit()
        flash('Usuário editado com sucesso', 'success')
        return redirect(url_for('main_bp.menu'))

    return render_template('administracao/form_edit.html', usuario=usuario)


@adm_bp.route('/listar_usuario', methods=['GET'])
@login_required
@role_required('admin')
def listar_usuario():
    usuarios = Usuario.query.all()
    return render_template('administracao/list.html', usuarios=usuarios)

@adm_bp.route('/deletar_usuario/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def deletar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario deletado com sucesso', 'success')
    return redirect(url_for('adm_bp.usuarios'))

@adm_bp.route("/filtra_usaurio", methods=["GET", "POST"])
def filtra_usaurio():
    query = request.args.get("q", "").strip()
    if query:
        usaurios = Usuario.query.filter(Usuario.nome.ilike(f"%{query}%")).limit(10).all()
        return jsonify([
            {"id": c.id, "nome": c.nome, "role": c.role, "email": c.email} 
            for c in usaurios
        ])
    return jsonify([])

