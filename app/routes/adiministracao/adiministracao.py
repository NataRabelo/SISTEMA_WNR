from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from app.utils.login_required import required_login
from app.utils.decorators import role_required
from app import bcrypt, db
from app.models import (EstadosCivis, 
                        GrauParentesco,
                        Sexo,
                        Situacao,
                        TipoEncaminhamento,
                        TipoMoradia,
                        Usuario,
                        CondicaoHabitacao,
                        TipoTransporte,
                        Escolaridade,
                        MetodoPagamento,)

adm_bp = Blueprint('adm_bp', __name__)


@adm_bp.route('/administracao', methods=['GET'])
@required_login
@role_required('admin')
def administracao():
    return render_template('administracao/menu.html')


@adm_bp.route('/opcoes', methods=['GET'])
@required_login
@role_required('admin')
def opcoes():
    sexos = Sexo.query.all()
    situacoes = Situacao.query.all()
    moradias = TipoMoradia.query.all()
    transportes = TipoTransporte.query.all()
    condicoes = CondicaoHabitacao.query.all()
    escolaridades = Escolaridade.query.all()
    pagamentos = MetodoPagamento.query.all()
    parentescos = GrauParentesco.query.all()
    tencaminhamentos = TipoEncaminhamento.query.all()
    estados = EstadosCivis.query.all()
    return render_template('administracao/menu_opcoes.html',
                           sexos=sexos,
                           situacoes=situacoes,
                           moradias=moradias,
                           transportes=transportes,
                           condicoes=condicoes,
                           escolaridades=escolaridades,
                           pagamentos=pagamentos,
                           parentescos=parentescos,
                           tencaminhamentos=tencaminhamentos,
                           estados=estados)

# SEXO


@adm_bp.route('/cadastrar_sexo', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def cadastrar_sexo():
    if request.method == 'POST':
        nome = request.form.get('nome')
        sexo = Sexo(
            nome=nome
        )
        db.session.add(sexo)
        db.session.commit()
        flash('Registro realizado com sucesso!', 'success')
        return redirect(url_for('adm_bp.opcoes'))
    return render_template('administracao/menu_opcoes.html')


@adm_bp.route('/editar_sexo/<int:id>', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def editar_sexo(id):
    sexo = Sexo.query.get_or_404(id)

    if request.method == 'POST':
        sexo.nome = request.form.get('nome')
        db.session.commit()
        flash('Sexo editado com sucesso', 'success')
        return redirect(url_for('adm_bp.opcoes'))

    return render_template('administracao/menu_opcoes.html', sexo=sexo)


@adm_bp.route('/listar_sexo', methods=['GET'])
@required_login
@role_required('admin')
def listar_sexo():
    sexos = Sexo.query.all()
    return render_template('administracao/menu_opcoes.html', sexos=sexos)


@adm_bp.route('/deletar_sexo/<int:id>', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def deletar_sexo(id):
    sexo = Sexo.query.get_or_404(id)
    db.session.delete(sexo)
    db.session.commit()
    flash('Sexo deletado com sucesso', 'success')
    return redirect(url_for('adm_bp.opcoes'))

# SITUACAO


@adm_bp.route('/cadastrar_situacao', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def cadastrar_situacao():
    if request.method == 'POST':
        nome = request.form.get('nome')
        situacao = Situacao(
            nome=nome
        )
        db.session.add(situacao)
        db.session.commit()
        flash('Registro realizado com sucesso!', 'success')
        return redirect(url_for('adm_bp.opcoes'))
    return render_template('administracao/menu_opcoes.html')


@adm_bp.route('/editar_situacao/<int:id>', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def editar_situacao(id):
    situacao = Situacao.query.get_or_404(id)

    if request.method == 'POST':
        situacao.nome = request.form.get('nome')
        db.session.commit()
        flash('situacao editado com sucesso', 'success')
        return redirect(url_for('adm_bp.opcoes'))

    return render_template('administracao/menu_opcoes.html', situacao=situacao)


@adm_bp.route('/listar_situacao', methods=['GET'])
@required_login
@role_required('admin')
def listar_situacao():
    situacoes = Situacao.query.all()
    return render_template('administracao/menu_opcoes.html', situacoes=situacoes)


@adm_bp.route('/deletar_situacao/<int:id>', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def deletar_situacao(id):
    situacao = Situacao.query.get_or_404(id)
    db.session.delete(situacao)
    db.session.commit()
    flash('Situação deletado com sucesso', 'success')
    return redirect(url_for('adm_bp.opcoes'))

# TIPO MORADIA


@adm_bp.route('/cadastrar_moradia', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def cadastrar_moradia():
    if request.method == 'POST':
        nome = request.form.get('nome')
        moradia = TipoMoradia(
            nome=nome
        )
        db.session.add(moradia)
        db.session.commit()
        flash('Registro realizado com sucesso!', 'success')
        return redirect(url_for('adm_bp.opcoes'))
    return render_template('administracao/menu_opcoes.html')


@adm_bp.route('/editar_moradia/<int:id>', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def editar_moradia(id):
    moradia = TipoMoradia.query.get_or_404(id)

    if request.method == 'POST':
        moradia.nome = request.form.get('nome')
        db.session.commit()
        flash('moradia editado com sucesso', 'success')
        return redirect(url_for('adm_bp.opcoes'))

    return render_template('administracao/menu_opcoes.html', moradia=moradia)


@adm_bp.route('/listar_moradia', methods=['GET'])
@required_login
@role_required('admin')
def listar_moradia():
    moradias = TipoMoradia.query.all()
    return render_template('administracao/menu_opcoes.html', moradias=moradias)


@adm_bp.route('/deletar_moradia/<int:id>', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def deletar_moradia(id):
    moradia = TipoMoradia.query.get_or_404(id)
    db.session.delete(moradia)
    db.session.commit()
    flash('Moradia deletado com sucesso', 'success')
    return redirect(url_for('adm_bp.opcoes'))

# CONDICAO HABITACAO


@adm_bp.route('/cadastrar_condicao', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def cadastrar_condicao():
    if request.method == 'POST':
        nome = request.form.get('nome')
        condicao = CondicaoHabitacao(
            nome=nome
        )
        db.session.add(condicao)
        db.session.commit()
        flash('Registro realizado com sucesso!', 'success')
        return redirect(url_for('adm_bp.opcoes'))
    return render_template('administracao/menu_opcoes.html')


@adm_bp.route('/editar_condicao/<int:id>', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def editar_condicao(id):
    condicao = CondicaoHabitacao.query.get_or_404(id)

    if request.method == 'POST':
        condicao.nome = request.form.get('nome')
        db.session.commit()
        flash('condicao editado com sucesso', 'success')
        return redirect(url_for('adm_bp.opcoes'))

    return render_template('administracao/menu_opcoes.html', condicao=condicao)


@adm_bp.route('/listar_condicao', methods=['GET'])
@required_login
@role_required('admin')
def listar_condicao():
    condicoes = CondicaoHabitacao.query.all()
    return render_template('administracao/menu_opcoes.html', condicoes=condicoes)


@adm_bp.route('/deletar_condicao/<int:id>', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def deletar_condicao(id):
    condicao = CondicaoHabitacao.query.get_or_404(id)
    db.session.delete(condicao)
    db.session.commit()
    flash('Condicao deletado com sucesso', 'success')
    return redirect(url_for('adm_bp.opcoes'))

# TIPO TRANSPORTE


@adm_bp.route('/cadastrar_transporte', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def cadastrar_transporte():
    if request.method == 'POST':
        nome = request.form.get('nome')
        transporte = TipoTransporte(
            nome=nome
        )
        db.session.add(transporte)
        db.session.commit()
        flash('Registro realizado com sucesso!', 'success')
        return redirect(url_for('adm_bp.opcoes'))
    return render_template('administracao/menu_opcoes.html')


@adm_bp.route('/editar_transporte/<int:id>', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def editar_transporte(id):
    transporte = TipoTransporte.query.get_or_404(id)

    if request.method == 'POST':
        transporte.nome = request.form.get('nome')
        db.session.commit()
        flash('transporte editado com sucesso', 'success')
        return redirect(url_for('adm_bp.opcoes'))
    return render_template('administracao/menu_opcoes.html', transporte=transporte)


@adm_bp.route('/listar_transporte', methods=['GET'])
@required_login
@role_required('admin')
def listar_transporte():
    transportes = TipoTransporte.query.all()
    return render_template('administracao/menu_opcoes.html', transportes=transportes)


@adm_bp.route('/deletar_transporte/<int:id>', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def deletar_transporte(id):
    transporte = TipoTransporte.query.get_or_404(id)
    db.session.delete(transporte)
    db.session.commit()
    flash('Transporte deletado com sucesso', 'success')
    return redirect(url_for('adm_bp.opcoes'))

# ESCOLARIEDADE


@adm_bp.route('/cadastrar_escolaridade', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def cadastrar_escolaridade():
    if request.method == 'POST':
        nome = request.form.get('nome')
        escolaridade = Escolaridade(
            nome=nome
        )
        db.session.add(escolaridade)
        db.session.commit()
        flash('Registro realizado com sucesso!', 'success')
        return redirect(url_for('adm_bp.opcoes'))
    return render_template('administracao/menu_opcoes.html')


@adm_bp.route('/editar_escolaridade/<int:id>', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def editar_escolaridade(id):
    escolaridade = Escolaridade.query.get_or_404(id)

    if request.method == 'POST':
        escolaridade.nome = request.form.get('nome')
        db.session.commit()
        flash('escolaridade editado com sucesso', 'success')
        return redirect(url_for('adm_bp.opcoes'))

    return render_template('administracao/menu_opcoes.html', escolaridade=escolaridade)


@adm_bp.route('/listar_escolaridade', methods=['GET'])
@required_login
@role_required('admin')
def listar_escolaridade():
    escolaridades = Escolaridade.query.all()
    return render_template('administracao/menu_opcoes.html', escolaridades=escolaridades)


@adm_bp.route('/deletar_escolaridade/<int:id>', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def deletar_escolaridade(id):
    escolaridade = Escolaridade.query.get_or_404(id)
    db.session.delete(escolaridade)
    db.session.commit()
    flash('Escolaridade deletado com sucesso', 'success')
    return redirect(url_for('adm_bp.opcoes'))


# METODO PAGAMENTO
@adm_bp.route('/cadastrar_pagamento', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def cadastrar_pagamento():
    if request.method == 'POST':
        nome = request.form.get('nome')
        juros = request.form.get('juros')
        pagamento = MetodoPagamento(
            nome=nome,
            juros=juros
        )
        db.session.add(pagamento)
        db.session.commit()
        flash('Registro realizado com sucesso!', 'success')
        return redirect(url_for('adm_bp.opcoes'))
    return render_template('administracao/menu_opcoes.html')


@adm_bp.route('/editar_pagamento/<int:id>', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def editar_pagamento(id):
    pagamento = MetodoPagamento.query.get_or_404(id)

    if request.method == 'POST':
        pagamento.nome = request.form.get('nome')
        pagamento.juros = request.form.get('juros')
        db.session.commit()
        flash('pagamento editado com sucesso', 'success')
        return redirect(url_for('adm_bp.opcoes'))

    return render_template('administracao/menu_opcoes.html', pagamento=pagamento)


@adm_bp.route('/listar_pagamento', methods=['GET'])
@required_login
@role_required('admin')
def listar_pagamento():
    pagamentos = MetodoPagamento.query.all()
    return render_template('administracao/menu_opcoes.html', pagamentos=pagamentos)


@adm_bp.route('/deletar_pagamento/<int:id>', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def deletar_pagamento(id):
    pagamento = MetodoPagamento.query.get_or_404(id)
    db.session.delete(pagamento)
    db.session.commit()
    flash('Pagamento deletado com sucesso', 'success')
    return redirect(url_for('adm_bp.opcoes'))

# GRAU PARENTESCO


@adm_bp.route('/cadastrar_parentesco', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def cadastrar_parentesco():
    if request.method == 'POST':
        nome = request.form.get('nome')
        grau = GrauParentesco(
            nome=nome
        )
        db.session.add(grau)
        db.session.commit()
        flash('Registro realizado com sucesso!', 'success')
        return redirect(url_for('adm_bp.opcoes'))
    return render_template('administracao/menu_opcoes.html')


@adm_bp.route('/editar_parentesco/<int:id>', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def editar_parentesco(id):
    grau = GrauParentesco.query.get_or_404(id)

    if request.method == 'POST':
        grau.nome = request.form.get('nome')
        db.session.commit()
        flash('grau editado com sucesso', 'success')
        return redirect(url_for('adm_bp.opcoes'))

    return render_template('administracao/menu_opcoes.html', grau=grau)


@adm_bp.route('/listar_parentesco', methods=['GET'])
@required_login
@role_required('admin')
def listar_parentesco():
    graus = GrauParentesco.query.all()
    return render_template('administracao/menu_opcoes.html', graus=graus)


@adm_bp.route('/deletar_parentesco/<int:id>', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def deletar_parentesco(id):
    grau = GrauParentesco.query.get_or_404(id)
    db.session.delete(grau)
    db.session.commit()
    flash('Grau de parentesco deletado com sucesso', 'success')
    return redirect(url_for('adm_bp.opcoes'))

# TIPO ENCAMINHAMENTO


@adm_bp.route('/cadastrar_tencaminhamento', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def cadastrar_tencaminhamento():
    if request.method == 'POST':
        nome = request.form.get('nome')
        tencaminhamento = TipoEncaminhamento(
            nome=nome
        )
        db.session.add(tencaminhamento)
        db.session.commit()
        return redirect(url_for('adm_bp.opcoes'))
    return render_template('administracao/menu_opcoes.html')


@adm_bp.route('/editar_tencaminhamento/<int:id>', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def editar_encaminhamento(id):
    tencaminhamento = TipoEncaminhamento.query.get_or_404(id)

    if request.method == 'POST':
        tencaminhamento.nome = request.form.get('nome')
        db.session.commit()
        flash('Tipo de encaminhamento atualizado com sucesso', 'success')
        return redirect(url_for('adm_bp.opcoes'))

    return render_template('administracao/menu_opcoes.html', tencaminhamento=tencaminhamento)


@adm_bp.route('/listar_tencaminhamento', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def listar_tencaminhamento():
    tencaminhamentos = TipoEncaminhamento.query.all()
    return render_template('administracao/menu_opcoes.html', tencaminhamentos=tencaminhamentos)


@adm_bp.route('/deletar_tencaminhamento/<int:id>', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def deletar_tencaminhamento(id):
    tencaminhamento = TipoEncaminhamento.query.get_or_404(id)
    db.session.delete(tencaminhamento)
    db.session.commit()
    flash('Tipo de encaminhamento deletado com sucesso', 'success')
    return redirect(url_for('adm_bp.opcoes'))


# ESTADO CIVIL 

@adm_bp.route('/cadastrar_estado', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def cadastrar_estado():
    if request.method == 'POST':
        nome = request.form.get('nome')
        estado = EstadosCivis(
            nome=nome
        )
        db.session.add(estado)
        db.session.commit()
        flash('Registro realizado com sucesso!', 'success')
        return redirect(url_for('adm_bp.opcoes'))
    return render_template('administracao/menu_opcoes.html')

@adm_bp.route('/editar_estado/<int:id>', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def editar_estado(id):
    estado = EstadosCivis.query.get_or_404(id)

    if request.method == 'POST':
        estado.nome = request.form.get('nome')
        db.session.commit()
        flash('Estado civil editado com sucesso', 'success')
        return redirect(url_for('adm_bp.opcoes'))

    return render_template('administracao/menu_opcoes.html', estado=estado)

@adm_bp.route('/listar_estado', methods=['GET'])
@required_login
@role_required('admin')
def listar_estado():
    estados = EstadosCivis.query.all()
    return render_template('administracao/menu_opcoes.html', estados=estados)

@adm_bp.route('/deletar_estado/<int:id>', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def deletar_estado(id):
    estado = EstadosCivis.query.get_or_404(id)
    db.session.delete(estado)
    db.session.commit()
    flash('Estado civil deletado com sucesso', 'success')
    return redirect(url_for('adm_bp.opcoes'))


# USUARIOS


@adm_bp.route('/usuarios', methods=['GET'])
@required_login
@role_required('admin')
def usuarios():
    return render_template('administracao/usuarios.html')


@adm_bp.route('/cadastrar_usuario', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        nome = request.form.get('name')
        email = request.form.get('email')
        senha = request.form.get('senha')
        role = request.form.get('role')
        print(nome, email, senha, role)

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
@required_login
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
@required_login
@role_required('admin')
def listar_usuario():
    usuarios = Usuario.query.all()
    return render_template('administracao/list.html', usuarios=usuarios)


@adm_bp.route('/deletar_usuario/<int:id>', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def deletar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario deletado com sucesso', 'success')
    return redirect(url_for('adm_bp.listar_usuario'))


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
