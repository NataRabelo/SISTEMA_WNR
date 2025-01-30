from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Cliente
from flask_login import login_required
from app import db
from datetime import datetime

client_bp = Blueprint('client_bp', __name__)

@client_bp.route('/cadastrar_cliente', methods=['GET','POST'])

def cadastrar_cliente():
    if request.method == 'POST':
        cliente = Cliente (
            nome = request.form.get('nome'),
            cpf = request.form.get('cpf'),
            email = request.form.get('email'),
            data_nascimento = datetime.strptime(request.form.get('dt_nascimento'),"%Y-%m-%d").date(),
            renda_familiar = request.form.get('renda_familiar'),
            bairro = request.form.get('bairro'),
            canal_divulgacao = request.form.get('canal_divulgacao'),
            cep = request.form.get('cep'),
            cidade = request.form.get('cidade'),
            condicao_habitacao = request.form.get('cidade'),
            cpf_responsavel = request.form.get('cpf_responsavel'),
            numero_cs = request.form.get('numero_cs'),
            despesa_mensal = request.form.get('despesa_mensal'),
            escolaridade = request.form.get('escolariedade'),
            estado = request.form.get('estado'),
            fone_contato = request.form.get('fone_contato'),
            fone_pessoal = request.form.get('fone_pessoal'),
            foto = request.form.get('foto'),
            grau_parentesco = request.form.get('grau_parentesco'),
            nome_plano_saude = request.form.get('nome_plano_saude'),
            nome_responsavel = request.form.get('nome_responsavel'),
            numero_filhos = request.form.get('numero_filhos'),
            plano_saude = request.form.get('plano_de_saude'),
            previdenciario = request.form.get('previdenciario'),
            profissao = request.form.get('profissao'),
            remuneracao = request.form.get('remuneracao'),
            rg = request.form.get('rg'),
            saldo = request.form.get('saldo'),
            sexo = request.form.get('sexo'),
            tipo_moradia = request.form.get('tipo_moradia'),
            transporte = request.form.get('transporte')
        )
        cpf = request.form.get('cpf')
        verifica_cliente = Cliente.query.filter_by(cpf=cpf).first()
        if verifica_cliente:
            flash('CPF já cadastrado', 'error')
            return redirect(url_for('main_bp.menu'))
        
        db.session.add(cliente)
        db.session.commit()
        flash('Cliente cadastrado com sucesso!', 'success')
    return render_template('clientes/form.html')

@client_bp.route('/listar_cliente', methods=['GET', 'POST'])
def listar_cliente():
    clientes = Cliente.query.all()
    return render_template('clientes/list.html', clientes=clientes)

@client_bp.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)

    if request.method == 'POST':
        # Atualiza os atributos do cliente existente
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
        cliente.condicao_habitacao = request.form.get('condicao_habitacao')  # Corrigido
        cliente.cpf_responsavel = request.form.get('cpf_responsavel')
        cliente.numero_cs = request.form.get('numero_cs')
        cliente.despesa_mensal = request.form.get('despesa_mensal')
        cliente.escolaridade = request.form.get('escolaridade')  # Corrigido
        cliente.estado = request.form.get('estado')
        cliente.fone_contato = request.form.get('fone_contato')
        cliente.fone_pessoal = request.form.get('fone_pessoal')
        cliente.foto = request.form.get('foto')
        cliente.grau_parentesco = request.form.get('grau_parentesco')
        cliente.nome_plano_saude = request.form.get('nome_plano_saude')
        cliente.nome_responsavel = request.form.get('nome_responsavel')
        cliente.numero_filhos = request.form.get('numero_filhos')
        cliente.plano_saude = request.form.get('plano_de_saude')
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
        return redirect(url_for('client_bp.listar_clientes'))  # Corrigido para um endpoint válido

    return render_template('clientes/form_edit.html', cliente=cliente)