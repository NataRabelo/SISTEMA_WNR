from datetime import datetime
from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_required
from app.models import Encaminhamento, Cliente, Profissional
from app import db 

encaminhamento_bp = Blueprint('encaminhamento_bp', __name__)

@encaminhamento_bp.route('/criar_encaminhamento', methods=['GET', 'POST'])
@login_required
def criar_encaminhamento():
    if request.method == 'POST':
        encaminhamento = Encaminhamento(
            cliente = request.form.get('cliente'),
            profissional = request.form.get('profissional'),
            convenio = request.form.get('convenio'),
            dias_horas_atendimento = request.form.get('dias_horas_atendimento'),
            data_encaminhamento = datetime(),
            observacoes_gerais = request.form.get('observacoes_gerais'),
            queixa = request.form.get('queixa'),
            situacao = request.form.get('situacao'),
            tipo_encaminhamento = request.form.get('tipo_encaminhamento'),
            valor = request.form.get('valor')
        )
        cliente = request.form.get('cliente')
        profissional = request.form.get('profissional')
        if cliente and profissional :
            flash('Encaminhamento com cliente e profissional já realizando')
            return redirect(url_for('main_bp.menu'))
        db.session.add(encaminhamento)
        db.session.commit()
        flash('Encaminhamento realizado com sucesso!', 'success')
    clientes = Cliente.query.all()
    profissionais = Profissional.query.all()
    return render_template('encaminhamento/form.html', clientes=clientes, profissionais=profissionais)

@encaminhamento_bp.route('/listar_encaminhamento', methods=['GET', 'POST'])
@login_required
def listar_encaminhamento():
    encaminhamentos = Encaminhamento.query.all()
    return render_template('encaminhamento/list.html', encaminhamentos=encaminhamentos)

@encaminhamento_bp.route('/editar_encaminhamento/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_encaminhamento(id):
    encaminhamento = Encaminhamento.query.get_or_404(id)
    if request.method == 'POST':
        encaminhamento.cliente = request.form.get('cliente')
        encaminhamento.profissional = request.form.get('profissional')
        encaminhamento.convenio = request.form.get('convenio')
        encaminhamento.dias_horas_atendimento = request.form.get('dias_horas_atendimento')
        encaminhamento.observacoes_gerais = request.form.get('observacoes_gerais')
        encaminhamento.queixa = request.form.get('queixa')
        encaminhamento.situacao = request.form.get('situacao')
        encaminhamento.tipo_encaminhamento = request.form.get('tipo_encaminhamento')
        encaminhamento.valor = request.form.get('valor')

        db.session.add(encaminhamento)
        db.session.commit()
        flash('Encaminhamento atualizado com sucesso!', 'success')
        return redirect(url_for('encaminhamento_bp.listar_encaminhamento'))
    return render_template('encaminhamento/form_edit.html')

@encaminhamento_bp.route('/deletar_encaminhamento/<int:id>')
@login_required
def deletar_encaminhamento(id):
    encaminhamento = Encaminhamento.query.get_or_404(id)
    db.session.delete(encaminhamento)
    db.session.commit()
    flash('Encaminhamento excluido com sucesso', 'success')
    return redirect(url_for('encaminhamento_bp.listar_profissional'))