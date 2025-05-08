from flask import Blueprint, flash, jsonify, render_template, request, redirect, url_for
from app.utils.editor_valor import converter_para_float
from app.utils.decorators import role_required
from flask_login import current_user
from app.models import Profissional
from datetime import datetime
from app import db
from app.utils.login_required import required_login

professional_bp = Blueprint('professional_bp', __name__)

@professional_bp.route('/profissional', methods=['GET', 'POST'])
@required_login
@role_required('atendimento', 'financeiro', 'admin')
def profissional():
    return render_template('profissional/professional.html')

@professional_bp.route('/cadastrar_profissional', methods=['GET', 'POST'])
@required_login
@role_required('atendimento', 'financeiro', 'admin')
def cadastrar_profissional():
    if request.method == 'POST':

        profissional = Profissional(
            nome                    = request.form.get('nome'),
            cpf                     = request.form.get('cpf'),
            email                   = request.form.get('email'),
            data_nascimento         = datetime.strptime(request.form.get('data_nascimento'),"%Y-%m-%d").date(),
            bairro                  = request.form.get('bairro'),
            banco                   = request.form.get('banco'),
            cep                     = request.form.get('cep'),
            cidade                  = request.form.get('cidade'),
            complemento             = request.form.get('complemento'),
            graduacao               = request.form.get('graduacao'),
            issqn                   = request.form.get('issqn'),
            fone_pessoal            = request.form.get('fone_pessoal'),
            fone_profissional       = request.form.get('fone_profissional'),
            curriculum_lattes       = request.form.get('curriculum_lattes'),
            dias_horas_disponiveis  = request.form.get('dias_horas_disponiveis'),
            endereco_profissional   = request.form.get('endereco_profissional'),
            estado                  = request.form.get('estado'),
            observacoes             = request.form.get('observacoes'),
            pix                     = request.form.get('pix'),
            registro_profissional   = request.form.get('registro_profissional'),
            rg                      = request.form.get('rg'),
            valor_minimo            = converter_para_float(request.form.get('valor_minimo'))
        )
        cpf = request.form.get('cpf')
        verifica_profissional = Profissional.query.filter_by(cpf=cpf).first()
        if verifica_profissional:
            flash('Profissional já cadastrado', 'error')
            return redirect(url_for('professional_bp.profissional'))
        
        db.session.add(profissional)
        db.session.commit()
        flash('Profissional cadastrado com sucesso!', 'success')
        return redirect(url_for('professional_bp.profissional'))
    return render_template('profissional/form.html')

@professional_bp.route('/listar_profissional', methods=['GET', 'POST'])
@required_login
@role_required('atendimento', 'financeiro', 'admin')
def listar_profissional():
    profissionais = Profissional.query.all()
    usuario = current_user
    return render_template('profissional/list.html', profissionais=profissionais, usuario=usuario)

@professional_bp.route('/editar_profissional/<int:id>', methods=['GET', 'POST'])
@required_login
@role_required('atendimento', 'financeiro', 'admin')
def editar_profissional(id):
    profissional = Profissional.query.get_or_404(id)
    if request.method == 'POST':

        profissional.nome                   = request.form.get('nome')
        profissional.cpf                    = request.form.get('cpf')
        profissional.email                  = request.form.get('email')
        data_nascimento                     = request.form.get('data_nascimento')
        if data_nascimento:
            profissional.data_nascimento    = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
        profissional.bairro                 = request.form.get('bairro')               
        profissional.banco                  = request.form.get('banco')                
        profissional.cep                    = request.form.get('cep')                  
        profissional.cidade                 = request.form.get('cidade')
        profissional.complemento            = request.form.get('complemento')              
        profissional.graduacao              = request.form.get('graduacao')            
        profissional.issqn                  = request.form.get('issqn')                
        profissional.fone_pessoal           = request.form.get('fone_pessoal')         
        profissional.fone_profissional      = request.form.get('fone_profissional')    
        profissional.foto                   = request.form.get('foto')                 
        profissional.curriculum_lattes      = request.form.get('curriculum_lattes')    
        profissional.dias_horas_disponivei  = request.form.get('dias_horas_disponiveis')
        profissional.endereco_profissional  = request.form.get('endereco_profissional')
        profissional.estado                 = request.form.get('estado')               
        profissional.observacoes            = request.form.get('observacoes')          
        profissional.pix                    = request.form.get('pix')                  
        profissional.registro_profissional  = request.form.get('registro_profissional')
        profissional.rg                     = request.form.get('rg')                   
        profissional.valor_minimo           = converter_para_float(request.form.get('valor_minimo'))

        db.session.add(profissional)
        db.session.commit()
        flash('Profissional atualizdo com sucesso!', 'success')
        return redirect(url_for('professional_bp.listar_profissional'))
    return render_template('profissional/form_edit.html', profissional=profissional)

@professional_bp.route('/deletar_profissional/<int:id>', methods=['GET', 'POST'])
@required_login
@role_required('admin')
def deletar_profissional(id):
    profissional = Profissional.query.get_or_404(id)
    db.session.delete(profissional)
    db.session.commit()
    flash('Profissional excluido com sucesso', 'success')
    return redirect(url_for('professional_bp.listar_profissional'))

@professional_bp.route("/filtra_profissional", methods=["GET", "POST"])
def filtra_profissional():
    query = request.args.get("q", "").strip()
    if query:
        profissionais = Profissional.query.filter(Profissional.nome.ilike(f"%{query}%")).limit(10).all()
        return jsonify([
            {"id": c.id, "nome": c.nome, "cpf": c.cpf, "email": c.email} 
            for c in profissionais
        ])
    return jsonify([])