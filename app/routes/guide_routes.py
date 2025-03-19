from datetime import datetime
from flask import Blueprint, flash, jsonify, render_template, request, redirect, url_for
from flask_login import login_required
from app.models import Cliente, Encaminhamento, Guia, Profissional
from app import db
from app.utils.decorators import role_required

guide_bp = Blueprint('guide_bp', __name__)

@guide_bp.route('/guia', methods=['GET', 'POST'])
@login_required
@role_required('atendimento', 'financeiro', 'admin')
def guia():
    return render_template('guides/guide.html')

@guide_bp.route('/emitir_guia', methods=['GET', 'POST'])
def emitir_guia():
    if request.method == 'POST':

        agora = datetime.now()  # Pega a data e hora local correta
        
        guia = Guia(
            client_id=request.form.get('client_id'),
            profissional_id=request.form.get('profissional_id'),
            data_original=agora,
            hora_emissao=agora.strftime('%H:%M:%S'),
            observacoes_gerais=request.form.get('observacoes_gerais'),
            quantidade_emissoes=request.form.get('quantidade_emissoes'),
            tipo_pagamento=request.form.get('tipo_pagamento'),
            valor_unitario=request.form.get('valor_unitario')
        )

        db.session.add(guia)
        db.session.commit()
        
    clientes = Cliente.query.all()
    profissionais = Profissional.query.all()
    return render_template('guides/form.html', clientes=clientes)

@guide_bp.route('/listar_guia', methods=['GET', 'POST'])
@login_required
@role_required('atendimento', 'financeiro', 'admin')
def listar_guia():
    guias = Guia.query.all()
    return render_template('guides/list.html', guias = guias)

@guide_bp.route('/editar_guia/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('financeiro', 'admin')
def editar_guia(id):
    guia = Guia.query.get_or_404(id)
    clientes = Cliente.query.all()
    profissionais = Profissional.query.all()

    if request.method == 'POST':
        guia.client_id = request.form.get('client_id')
        guia.profissional_id = request.form.get('profissional_id')
        guia.observacoes_gerais = request.form.get('observacoes_gerais')
        guia.quantidade_emissoes = request.form.get('quantidade_emissoes')
        guia.tipo_pagamento = request.form.get('tipo_pagamento')
        guia.valor_unitario = request.form.get('valor_unitario')

        db.session.commit()
        flash('Guia atualizada com sucessso', 'success')
    return render_template('guides/form_edit.html', guia = guia, clientes=clientes, profissionais=profissionais)

@guide_bp.route('/deletar_guia/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def deletar_guia(id):
    guia = Guia.query.get_or_404(id)
    db.session.delete(guia)
    db.session.commit()
    flash('Guia deletada com sucesso', 'success')
    return redirect(url_for('guide_bp.listar_guia'))

# Essa rota ficará aqui pois a mesma é utilizada na tela de emissão de guia
@guide_bp.route('/buscar_profissionais/<int:cliente_id>', methods=['GET'])
def buscar_profissionais(cliente_id):
    encaminhamentos = Encaminhamento.query.filter_by(cliente_id=cliente_id).all()
    profissionais = [profissional for enc in encaminhamentos for profissional in Profissional.query.filter_by(id=enc.profissional_id).all()]

    return jsonify({
        "profissionais": [{"id": p.id, "nome": p.nome} for p in profissionais]
    })
