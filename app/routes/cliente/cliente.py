from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from app.utils import calcular_idade
from app.utils.editor_valor import converter_para_float, formatar_para_moeda
from app.utils.decorators import role_required
from flask_login import current_user, login_required
from app.models import Cliente
from datetime import datetime
from app import db


client_bp = Blueprint('client_bp', __name__)

@client_bp.route('/cliente', methods=['GET', 'POST'])
@login_required
@role_required('atendimento', 'financeiro', 'admin')
def cliente():
    return render_template('clientes/cliente.html')

@client_bp.route('/cadastrar_cliente', methods=['GET','POST'])
@login_required
@role_required('atendimento', 'financeiro', 'admin')
def cadastrar_cliente():
    if request.method == 'POST':
        idade = request.form.get('idade')
        print(idade)
        cliente = Cliente(
            nome                = request.form.get('nome'),
            cpf                 = request.form.get('cpf'),
            email               = request.form.get('email'),
            data_nascimento     = datetime.strptime(request.form.get('dt_nascimento'),"%Y-%m-%d").date(),
            renda_familiar      = converter_para_float(request.form.get('renda_familiar')),
            bairro              = request.form.get('bairro'),
            canal_divulgacao    = request.form.get('canal_divulgacao'),
            cep                 = request.form.get('cep'),
            cidade              = request.form.get('cidade'),
            condicao_habitacao  = request.form.get('condicao_habitacao'),
            cpf_responsavel     = request.form.get('cpf_responsavel'),
            complemento         = request.form.get('complemento'),
            numero_cs           = request.form.get('numero_cs'),
            despesa_mensal      = converter_para_float(request.form.get('despesa_mensal')),
            escolaridade        = request.form.get('escolaridade'),
            estado              = request.form.get('estado'),
            endereco            = request.form.get('endereco'),
            fone_contato        = request.form.get('fone_contato'),
            fone_pessoal        = request.form.get('fone_pessoal'),
            foto                = request.form.get('foto'),
            grau_parentesco     = request.form.get('grau_parentesco'),
            nome_plano_saude    = request.form.get('nome_plano_saude'),
            nome_responsavel    = request.form.get('nome_responsavel'),
            possui_filhos        = request.form.get('possui_filhos'),
            numero_filhos       = request.form.get('numero_filhos'),
            plano_saude         = request.form.get('plano_saude'),
            previdenciario      = request.form.get('previdenciario'),
            profissao           = request.form.get('profissao'),
            remuneracao         = converter_para_float(request.form.get('remuneracao')),
            rg                  = request.form.get('rg'),
            saldo               = converter_para_float(request.form.get('saldo')),
            sexo                = request.form.get('sexo'),
            tipo_moradia        = request.form.get('tipo_moradia'),
            transporte          = request.form.get('transporte'),
            idade               = int(request.form.get('idade'))
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
    
    return render_template('clientes/form.html')

@client_bp.route('/listar_cliente', methods=['GET', 'POST'])
@login_required
@role_required('atendimento', 'financeiro', 'admin')
def listar_cliente():
    clientes = Cliente.query.all()
    usuario = current_user
    return render_template('clientes/list.html', clientes=clientes, usuario=usuario)

@client_bp.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('atendimento', 'financeiro', 'admin')
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    remuneracao_formatada = formatar_para_moeda(cliente.remuneracao)
    renda_familiar_formatada = formatar_para_moeda(cliente.renda_familiar)
    despesa_mensal_formatada = formatar_para_moeda(cliente.despesa_mensal)
    if cliente.idade is None:
        idade = 00
    else :
        idade = int(cliente.idade)

    print(idade)
    if request.method == 'POST':

        idade = request.form.get('idade')

        cliente.nome = request.form.get('nome')
        cliente.cpf = request.form.get('cpf')
        cliente.email = request.form.get('email')
        data_nascimento = request.form.get('dt_nascimento')
        cliente.idade = request.form.get('idade')
        if data_nascimento:
            cliente.data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
        cliente.renda_familiar = converter_para_float(request.form.get('renda_familiar'))
        cliente.bairro = request.form.get('bairro')
        cliente.canal_divulgacao = request.form.get('canal_divulgacao')
        cliente.cep = request.form.get('cep')
        cliente.cidade = request.form.get('cidade')
        cliente.condicao_habitacao = request.form.get('condicao_habitacao')  
        cliente.cpf_responsavel = request.form.get('cpf_responsavel')
        cliente.complemento = request.form.get('complemento')
        cliente.numero_cs = request.form.get('numero_cs')
        cliente.despesa_mensal = converter_para_float(request.form.get('despesa_mensal'))
        cliente.escolaridade = request.form.get('escolaridade')  
        cliente.estado = request.form.get('estado')
        cliente.endereco = request.form.get('endereco')
        cliente.fone_contato = request.form.get('fone_contato')
        cliente.fone_pessoal = request.form.get('fone_pessoal')
        cliente.foto = request.form.get('foto')
        cliente.grau_parentesco = request.form.get('grau_parentesco')
        cliente.nome_responsavel = request.form.get('nome_responsavel')
        
        numero_filhos = request.form.get('numero_filhos')
        possui_filhos = request.form.get('possui_filhos')
        if possui_filhos == 'Não':
            cliente.numero_filhos = 0
            cliente.possui_filhos = possui_filhos
        elif possui_filhos == 'Sim':
            cliente.numero_filhos = numero_filhos
            cliente.possui_filhos = possui_filhos

        nome_plano_saude = request.form.get('nome_plano_saude')    
        plano_saude = request.form.get('plano_saude')
        if plano_saude == 'Sim':
            cliente.nome_plano_saude = nome_plano_saude
            cliente.plano_saude = plano_saude
        elif plano_saude == 'Não':
            cliente.nome_plano_saude = 'Sem plano de Saúde'
            cliente.plano_saude = plano_saude

        cliente.previdenciario = request.form.get('previdenciario')
        cliente.profissao = request.form.get('profissao')
        cliente.remuneracao = converter_para_float(request.form.get('remuneracao'))
        cliente.rg = request.form.get('rg')
        cliente.saldo = converter_para_float(request.form.get('saldo'))
        cliente.sexo = request.form.get('sexo')
        cliente.tipo_moradia = request.form.get('tipo_moradia')
        cliente.transporte = request.form.get('transporte')

        db.session.commit()
        flash('Cliente atualizado com sucesso!', 'success')
        return redirect(url_for('client_bp.listar_cliente'))  

    return render_template('clientes/form_edit.html', cliente=cliente, remuneracao=remuneracao_formatada, renda_familiar=renda_familiar_formatada, despesa_mensal=despesa_mensal_formatada, idade=idade)

@client_bp.route('/deletar_cliente/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def deletar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    flash('Cliente excluido com sucesso', 'success')
    return redirect(url_for('client_bp.listar_cliente'))

@client_bp.route("/filtra_cliente", methods=["GET", "POST"])
def filtra_cliente():
    query = request.args.get("q", "").strip()
    if query:
        clientes = Cliente.query.filter(Cliente.nome.ilike(f"%{query}%")).limit(10).all()
        return jsonify([
            {"id": c.id, "nome": c.nome, "cpf": c.cpf, "email": c.email} 
            for c in clientes
        ])
    return jsonify([])