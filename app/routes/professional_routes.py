from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_required
from app.models import Profissional
from datetime import datetime
from app import db

professional_bp = Blueprint('professional_bp', __name__)

@professional_bp.route('/cadastrar_profissional', methods=['GET', 'POST'])
@login_required
def cadastrar_profissional():
    if request.method == 'POST':
        profissional = Profissional(
            nome = request.form.get('nome'),
            cpf = request.form.get('cpf'),
            email = request.form.get('email'),
            data_nascimento = datetime.strptime(request.form.get('data_nascimento'),"%Y-%m-%d").date(),
            bairro = request.form.get('bairro'),
            banco = request.form.get('banco'),
            cep = request.form.get('cep'),
            cidade = request.form.get('cidade'),
            graduacao = request.form.get('graduacao'),
            issqn = request.form.get('issqn'),
            fone_pessoal = request.form.get('fone_pessoal'),
            fone_profissional = request.form.get('fone_profissional'),
            foto = request.form.get('foto'),
            curriculum_lattes = request.form.get('curriculum_lattes'),
            dias_horas_disponiveis = request.form.get('dias_horas_disponiveis'),
            endereco_profissional = request.form.get('endereco_profissional'),
            estado = request.form.get('estado'),
            observacoes = request.form.get('observacoes'),
            pix = request.form.get('pix'),
            registro_profissional = request.form.get('registro_profissional'),
            rg = request.form.get('rg'),
            valor_minimo = request.form.get('valor_minimo')
        )
        cpf = request.form.get('cpf')
        verifica_profissional = Profissional.query.filter_by(cpf=cpf).first()
        if verifica_profissional:
            flash('Profissional já cadastrado', 'error')
            return redirect(url_for('main_bp.menu'))
        
        db.session.add(profissional)
        db.session.commit()
        flash('Profissional cadastrado com sucesso!', 'success')
    return render_template('professional/form.html')

@professional_bp.route('/listar_profissional', methods=['GET', 'POST'])
@login_required
def listar_profissional():
    profissionais = Profissional.query.all()
    return render_template('professional/list.html', profissionais=profissionais)
