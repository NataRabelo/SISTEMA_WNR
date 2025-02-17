from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from app.utils.edit_values import limpar_valor
from app.utils.decorators import role_required
from flask_login import login_required
from app.models import Cliente
from datetime import datetime
from app import db


client_bp = Blueprint('client_bp', __name__)

@client_bp.route('/cadastrar_cliente', methods=['GET','POST'])
@login_required
@role_required('atendimento', 'financeiro', 'admin')
def cadastrar_cliente():
    if request.method == 'POST':
        cliente = Cliente(
            nome                = request.form.get('nome'),
            cpf                 = request.form.get('cpf'),
            email               = request.form.get('email'),
            data_nascimento     = datetime.strptime(request.form.get('dt_nascimento'),"%Y-%m-%d").date(),
            renda_familiar      = limpar_valor(request.form.get('renda_familiar')),
            bairro              = request.form.get('bairro'),
            canal_divulgacao    = request.form.get('canal_divulgacao'),
            cep                 = request.form.get('cep'),
            cidade              = request.form.get('cidade'),
            condicao_habitacao  = request.form.get('condicao_habitacao'),
            cpf_responsavel     = request.form.get('cpf_responsavel'),
            numero_cs           = request.form.get('numero_cs'),
            despesa_mensal      = limpar_valor(request.form.get('despesa_mensal')),
            escolaridade        = request.form.get('escolariedade'),
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
            remuneracao         = limpar_valor(request.form.get('remuneracao')),
            rg                  = request.form.get('rg'),
            saldo               = limpar_valor(request.form.get('saldo')),
            sexo                = request.form.get('sexo'),
            tipo_moradia        = request.form.get('tipo_moradia'),
            transporte          = request.form.get('transporte')
        )
        
        cpf = request.form.get('cpf')
        verifica_cpf = Cliente.query.filter_by(cpf=cpf).first()
        
        email = request.form.get('email')
        verifica_email = Cliente.query.filter_by(email=email).first()

        if verifica_cpf and verifica_email:
            flash('Cliente já cadastrado', 'error')
            return redirect(url_for('main_bp.menu'))
        
        db.session.add(cliente)
        db.session.commit()
        flash("Cadastro realizado com sucesso!", "success")  # Mensagem de sucesso com categoria
        return redirect(url_for('main_bp.menu'))
    
    return render_template('clientes/form.html')

@client_bp.route('/listar_cliente', methods=['GET', 'POST'])
@login_required
@role_required('atendimento', 'financeiro', 'admin')
def listar_cliente():
    clientes = Cliente.query.all()
    return render_template('clientes/list.html', clientes=clientes)

@client_bp.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('atendimento', 'financeiro', 'admin')
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)

    if request.method == 'POST':

        cliente.nome = request.form.get('nome')
        cliente.cpf = request.form.get('cpf')
        cliente.email = request.form.get('email')
        data_nascimento = request.form.get('dt_nascimento')
        if data_nascimento:
            cliente.data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
        cliente.renda_familiar = request.form.get('renda_familiar')
        cliente.bairro = request.form.get('bairro')
        cliente.canal_divulgacao = request.form.get('canal_divulgacao')
        cliente.cep = request.form.get('cep')
        cliente.cidade = request.form.get('cidade')
        cliente.condicao_habitacao = request.form.get('condicao_habitacao')  
        cliente.cpf_responsavel = request.form.get('cpf_responsavel')
        cliente.numero_cs = request.form.get('numero_cs')
        cliente.despesa_mensal = request.form.get('despesa_mensal')
        cliente.escolariedade = request.form.get('escolariedade')  
        cliente.estado = request.form.get('estado')
        cliente.endereco = request.form.get('endereco')
        cliente.fone_contato = request.form.get('fone_contato')
        cliente.fone_pessoal = request.form.get('fone_pessoal')
        cliente.foto = request.form.get('foto')
        cliente.grau_parentesco = request.form.get('grau_parentesco')
        cliente.nome_plano_saude = request.form.get('nome_plano_saude')
        cliente.nome_responsavel = request.form.get('nome_responsavel')
        cliente.possui_filhos = request.form.get('possui_filhos')
        cliente.numero_filhos = request.form.get('numero_filhos')
        cliente.plano_saude = request.form.get('plano_saude')
        cliente.previdenciario = request.form.get('previdenciario')
        cliente.profissao = request.form.get('profissao')
        cliente.remuneracao = request.form.get('remuneracao')
        cliente.rg = request.form.get('rg')
        cliente.saldo = request.form.get('saldo')
        cliente.sexo = request.form.get('sexo')
        cliente.tipo_moradia = request.form.get('tipo_moradia')
        cliente.transporte = request.form.get('transporte')

        db.session.commit()
        flash('Cliente atualizado com sucesso!', 'success')
        return redirect(url_for('client_bp.listar_cliente'))  

    return render_template('clientes/form_edit.html', cliente=cliente)

@client_bp.route('/deletar_cliente/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def deletar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    flash('Cliente excluido com sucesso', 'success')
    return redirect(url_for('client_bp.listar_cliente'))

@client_bp.route('/buscar_cliente', methods=['GET'])
def buscar_cliente():
    codigo = request.args.get('codigo')
    cliente = Cliente.query.filter_by(id=codigo).first()
    if cliente:
        return jsonify({'nome': cliente.nome})
    return jsonify({'erro': 'Cliente não encontrado'}), 404