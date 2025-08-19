from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from app.utils.editor_valor import converter_para_float, formatar_para_moeda
from app.utils.limpa_valor import limpar_mascara
from app.utils.login_required import required_login
from app.utils.decorators import role_required
from flask_login import current_user
from datetime import datetime
from app import db
from app.models import (Cliente,
                        CondicaoHabitacao,
                        Escolaridade, EstadosCivis,
                        GrauParentesco,
                        Sexo,
                        TipoMoradia,
                        TipoTransporte)


client_bp = Blueprint('client_bp', __name__)


@client_bp.route('/cliente', methods=['GET', 'POST'])
@required_login
@role_required('atendimento', 'financeiro', 'admin')
def cliente():
    return render_template('clientes/cliente.html')


@client_bp.route('/cadastrar_cliente', methods=['GET', 'POST'])
@required_login
@role_required('atendimento', 'financeiro', 'admin')
def cadastrar_cliente():
    sexos           = Sexo.query.all()
    condicoes       = CondicaoHabitacao.query.all()
    moradias        = TipoMoradia.query.all()
    transportes     = TipoTransporte.query.all()
    escolaridades   = Escolaridade.query.all()
    parentescos     = GrauParentesco.query.all()
    estados         = EstadosCivis.query.all()

    if request.method == 'POST':
        cliente = Cliente(
            nome                        = request.form.get('nome'),
            cpf                         = limpar_mascara(request.form.get('cpf')),
            email                       = request.form.get('email'),
            bairro                      = request.form.get('bairro'),
            canal_divulgacao            = request.form.get('canal_divulgacao'),
            cep                         = limpar_mascara(request.form.get('cep')),
            cidade                      = request.form.get('cidade'),
            cpf_responsavel             = request.form.get('cpf_responsavel'),
            complemento                 = request.form.get('complemento'),
            numero_cs                   = request.form.get('numero_cs'),
            estado                      = request.form.get('estado'),
            endereco                    = request.form.get('endereco'),
            fone_contato                = limpar_mascara(request.form.get('fone_contato')),
            fone_pessoal                = limpar_mascara(request.form.get('fone_pessoal')),
            nome_plano_saude            = request.form.get('nome_plano_saude'),
            nome_responsavel            = request.form.get('nome_responsavel'),
            possui_filhos               = request.form.get('possui_filhos'),
            numero_filhos               = request.form.get('numero_filhos'),
            plano_saude                 = request.form.get('plano_saude'),
            previdenciario              = request.form.get('previdenciario'),
            profissao                   = request.form.get('profissao'),
            rg                          = request.form.get('rg'),
            grau_parentesco_id          = request.form.get('grau_parentesco'),
            estado_civil_id             = request.form.get('estado_civil'),
            renda_familiar              = converter_para_float(request.form.get('renda_familiar')),
            despesa_mensal              = converter_para_float(request.form.get('despesa_mensal')),
            remuneracao                 = converter_para_float(request.form.get('remuneracao')),
            saldo                       = converter_para_float(request.form.get('saldo')),
            idade                       = int(request.form.get('idade')),
            sexo_id                     = int(request.form.get('sexo')),
            condicao_habitacao_id       = int(request.form.get('condicao_habitacao')),
            tipo_moradia_id             = int(request.form.get('tipo_moradia')),
            tipo_transporte_id          = int(request.form.get('transporte')),
            escolaridade_id             = int(request.form.get('escolaridade')),
            data_nascimento             = datetime.strptime(request.form.get('dt_nascimento'), "%Y-%m-%d").date()
        )

        cpf = request.form.get('cpf')
        verifica_cpf = Cliente.query.filter_by(cpf=cpf).first()

        if verifica_cpf:
            flash('Cliente já cadastrado', 'error')
            return redirect(url_for('client_bp.cliente'))

        db.session.add(cliente)
        db.session.commit()
        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for('client_bp.cliente'))

    return render_template('clientes/form.html',
                           sexos=sexos,
                           condicoes=condicoes,
                           moradias=moradias,
                           transportes=transportes,
                           escolaridades=escolaridades,
                           parentescos=parentescos,
                           estados=estados)


@client_bp.route('/listar_cliente', methods=['GET', 'POST'])
@required_login
@role_required('atendimento', 'financeiro', 'admin')
def listar_cliente():
    clientes = Cliente.query.all()
    usuario = current_user
    return render_template('clientes/list.html', clientes=clientes, usuario=usuario)


@client_bp.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
@required_login
@role_required('atendimento', 'financeiro', 'admin')
def editar_cliente(id):
    sexos                               = Sexo.query.all()
    condicoes                           = CondicaoHabitacao.query.all()
    moradias                            = TipoMoradia.query.all()
    transportes                         = TipoTransporte.query.all()
    escolaridades                       = Escolaridade.query.all()
    parentescos                         = GrauParentesco.query.all()
    estados                             = EstadosCivis.query.all()
    cliente                             = Cliente.query.get_or_404(id)
    remuneracao_formatada               = formatar_para_moeda(cliente.remuneracao)
    renda_familiar_formatada            = formatar_para_moeda(cliente.renda_familiar)
    despesa_mensal_formatada            = formatar_para_moeda(cliente.despesa_mensal)
    saldo_formatado                     = formatar_para_moeda(cliente.saldo)

    cpf_limpo       = request.form.get('cpf')
    celular_limpo   = request.form.get('fone_pessoal')
    telefone_limpo  = request.form.get('fone_contato')
    cep_limpo       = request.form.get('cep')

    if request.method == 'POST':
        sexos                           = Sexo.query.all()
        condicoes                       = CondicaoHabitacao.query.all()
        moradias                        = TipoMoradia.query.all()
        transportes                     = TipoTransporte.query.all()
        escolaridades                   = Escolaridade.query.all()
        parentescos                     = GrauParentesco.query.all()
        estados                         = EstadosCivis.query.all()

        cliente.idade                   = request.form.get('idade')
        cliente.nome                    = request.form.get('nome')
        cliente.cpf                     = cpf_limpo
        cliente.email                   = request.form.get('email')
        data_nascimento                 = request.form.get('dt_nascimento')
        cliente.idade                   = request.form.get('idade')
        cliente.bairro                  = request.form.get('bairro')
        cliente.canal_divulgacao        = request.form.get('canal_divulgacao')
        cliente.cep                     = cep_limpo
        cliente.cidade                  = request.form.get('cidade')
        cliente.condicao_habitacao_id   = request.form.get('condicao_habitacao')
        cliente.cpf_responsavel         = request.form.get('cpf_responsavel')
        cliente.complemento             = request.form.get('complemento')
        cliente.numero_cs               = request.form.get('numero_cs')
        cliente.escolaridade_id         = request.form.get('escolaridade')
        cliente.estado                  = request.form.get('estado')
        cliente.endereco                = request.form.get('endereco')
        cliente.fone_contato            = telefone_limpo
        cliente.fone_pessoal            = celular_limpo
        cliente.grau_parentesco_id      = request.form.get('grau_parentesco')
        cliente.nome_responsavel        = request.form.get('nome_responsavel')
        numero_filhos                   = request.form.get('numero_filhos')
        possui_filhos                   = request.form.get('possui_filhos')
        nome_plano_saude                = request.form.get('nome_plano_saude')
        plano_saude                     = request.form.get('plano_saude')
        cliente.previdenciario          = request.form.get('previdenciario')
        cliente.profissao               = request.form.get('profissao')
        cliente.rg                      = request.form.get('rg')
        cliente.sexo_id                 = request.form.get('sexo')
        cliente.tipo_moradia_id         = request.form.get('tipo_moradia')
        cliente.transporte_id           = request.form.get('transporte')

        cliente.saldo                   = converter_para_float(request.form.get('saldo'))
        cliente.remuneracao             = converter_para_float(request.form.get('remuneracao'))
        cliente.despesa_mensal          = converter_para_float(request.form.get('despesa_mensal'))
        cliente.renda_familiar          = converter_para_float(request.form.get('renda_familiar'))

        # Lógica para verificar se o campo 'idade' foi preenchido
        if data_nascimento:
            cliente.data_nascimento     = datetime.strptime(data_nascimento, "%Y-%m-%d").date()

        # Lógica para verificar se o campo 'possui_filhos' foi preenchido
        if possui_filhos == 'Não':
            cliente.numero_filhos = 0
            cliente.possui_filhos = possui_filhos
        elif possui_filhos == 'Sim':
            cliente.numero_filhos = numero_filhos
            cliente.possui_filhos = possui_filhos

        # Lógica para verificar se o campo 'plano_saude' foi preenchido
        if plano_saude == 'Sim':
            cliente.nome_plano_saude = nome_plano_saude
            cliente.plano_saude = plano_saude
        elif plano_saude == 'Não':
            cliente.nome_plano_saude = 'Sem plano de Saúde'
            cliente.plano_saude = plano_saude

        
        db.session.commit()
        flash('Cliente atualizado com sucesso!', 'success')
        return redirect(url_for('client_bp.listar_cliente'))

    return render_template('clientes/form_edit.html',
                           cliente=cliente,
                           remuneracao=remuneracao_formatada,
                           renda_familiar=renda_familiar_formatada,
                           despesa_mensal=despesa_mensal_formatada,
                           saldo_formatado=saldo_formatado,
                           sexos=sexos,
                           condicoes=condicoes,
                           moradias=moradias,
                           transportes=transportes,
                           escolaridades=escolaridades,
                           parentescos=parentescos,
                           estados=estados)


@client_bp.route('/deletar_cliente/<int:id>', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def deletar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    flash('Cliente excluido com sucesso', 'success')
    return redirect(url_for('client_bp.listar_cliente'))


@client_bp.route("/filtra_cliente", methods=["GET", "POST"])
@required_login
def filtra_cliente():
    query = request.args.get("q", "").strip()
    if query:
        clientes = Cliente.query.filter(Cliente.nome.ilike(f"%{query}%")).limit(10).all()
        return jsonify([
            {"id": c.id, "nome": c.nome, "cpf": c.cpf, "email": c.email, "contato": c.fone_contato}
            for c in clientes
        ])
    return jsonify([])
