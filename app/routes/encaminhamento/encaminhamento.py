from flask import Blueprint, flash, jsonify, render_template, request, redirect, url_for
from app.models import Encaminhamento, Cliente, Profissional, Situacao, TipoEncaminhamento
from app.utils.decorators import role_required 
from flask_login import current_user
from datetime import datetime
from app import db
from app.utils.editor_valor import converter_para_float, formatar_para_moeda
from app.utils.login_required import required_login


encaminhamento_bp = Blueprint('encaminhamento_bp', __name__)

@encaminhamento_bp.route('/encaminhamento', methods=['GET', 'POST'])
@required_login
@role_required('atendimento', 'financeiro', 'admin')
def encaminhamento():
    return render_template('encaminhamento/encaminhamento.html')

@encaminhamento_bp.route('/criar_encaminhamento', methods=['GET', 'POST'])
@required_login
@role_required('atendimento', 'financeiro', 'admin')
def criar_encaminhamento():
    situacoes = Situacao.query.all()
    tencaminhamentos = TipoEncaminhamento.query.all()

    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        profissional_id = request.form.get('profissional_id')

        if not cliente_id or not profissional_id:
            flash('Erro: Cliente e profissional são obrigatórios!', 'danger')
            return redirect(url_for('encaminhamento_bp.criar_encaminhamento'))

        encaminhamento = Encaminhamento(
            cliente_id=cliente_id,
            profissional_id=profissional_id,
            convenio=request.form.get('convenio'),
            dias_horas_atendimento=request.form.get('dias_horas_atendimento'),
            data_encaminhamento=datetime.utcnow(),
            observacoes_gerais=request.form.get('observacoes_gerais'),
            queixa= request.form.get('queixa'),
            situacao_id=int(request.form.get('situacao')),
            tipo_encaminhamento_id=int(request.form.get('tipo_encaminhamento')),
            valor= converter_para_float(request.form.get('valor'))
        )

        verifica_encaminnhamento = Encaminhamento.query.filter_by(cliente_id=cliente_id, profissional_id=profissional_id).first()

        if verifica_encaminnhamento:
            flash('Cliente já encaminhado para esse profissional', 'danger')
            return redirect(url_for('encaminhamento_bp.encaminhamento'))

        db.session.add(encaminhamento)
        db.session.commit()
        flash('Encaminhamento realizado com sucesso!', 'success')
        return redirect(url_for('encaminhamento_bp.encaminhamento'))

    clientes = Cliente.query.all()
    profissionais = Profissional.query.all()
    return render_template('encaminhamento/form.html',
                            clientes=clientes,
                            profissionais=profissionais,
                            tencaminhamentos=tencaminhamentos,
                            situacoes=situacoes)

@encaminhamento_bp.route('/listar_encaminhamento', methods=['GET', 'POST'])
@required_login
@role_required('atendimento', 'financeiro', 'admin')
def listar_encaminhamento():
    encaminhamentos = Encaminhamento.query.all()
    usuario = current_user
    return render_template('encaminhamento/list.html', encaminhamentos=encaminhamentos, usuario=usuario)

@encaminhamento_bp.route('/editar_encaminhamento/<int:id>', methods=['GET', 'POST'])
@required_login
@role_required('atendimento', 'financeiro', 'admin')
def editar_encaminhamento(id):
    tencaminhameos = TipoEncaminhamento.query.all()
    situacoes = Situacao.query.all()
    encaminhamento = Encaminhamento.query.get_or_404(id)
    clientes = Cliente.query.all()
    profissionais = Profissional.query.all()
    valor_formatado = formatar_para_moeda(encaminhamento.valor)

    if request.method == 'POST':
        encaminhamento.cliente_id = request.form.get('cliente_id')
        encaminhamento.profissional_id = request.form.get('profissional_id')
        encaminhamento.convenio = request.form.get('convenio')
        encaminhamento.dias_horas_atendimento = request.form.get('dias_horas_atendimento')
        encaminhamento.observacoes_gerais = request.form.get('observacoes_gerais')
        encaminhamento.queixa = request.form.get('queixa')
        encaminhamento.situacao_id = int(request.form.get('situacao'))
        encaminhamento.tipo_encaminhamento_id = int(request.form.get('tipo_encaminhamento'))
        encaminhamento.valor = converter_para_float(request.form.get('valor'))
        
        db.session.commit()
        flash('Encaminhamento atualizado com sucesso!', 'success')
        return redirect(url_for('encaminhamento_bp.listar_encaminhamento'))
    return render_template(
        'encaminhamento/form_edit.html',
        encaminhamento=encaminhamento,
        clientes=clientes,
        profissionais=profissionais,
        valor_formatado=valor_formatado,
        tencaminhamentos=tencaminhameos,
        situacoes=situacoes)

@encaminhamento_bp.route('/deletar_encaminhamento/<int:id>')
@required_login
@role_required('admin')
def deletar_encaminhamento(id):
    encaminhamento = Encaminhamento.query.get_or_404(id)
    db.session.delete(encaminhamento)
    db.session.commit()
    flash('Encaminhamento excluido com sucesso', 'success')
    return redirect(url_for('encaminhamento_bp.listar_encaminhamento'))

@encaminhamento_bp.route("/filtra_encaminhamento", methods=["GET", "POST"])
def filtra_encaminhamento():
    query = request.args.get("q", "").strip()
    
    if query:
        encaminhamentos = (
            Encaminhamento.query
            .join(Cliente)  # Se necessário, unir a tabela Cliente
            .filter(Cliente.nome.ilike(f"%{query}%"))
            .limit(10)
            .all()
        )

        return jsonify([
            {
                "id": c.id,
                "nome": c.cliente.nome,  # Acessando o nome pelo relacionamento
                "profissional": c.profissional.nome
            } 
            for c in encaminhamentos
        ])
    
    return jsonify([])
