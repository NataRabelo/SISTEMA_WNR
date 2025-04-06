from datetime import datetime
from flask import Blueprint, flash, jsonify, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from app.models import Cliente, Encaminhamento, Guia, Profissional
from app import db
from app.utils.decorators import role_required
from app.utils.edit_values import converter_para_float, formatar_para_moeda

guide_bp = Blueprint('guide_bp', __name__)

@guide_bp.route('/guia', methods=['GET', 'POST'])
@login_required
@role_required('atendimento', 'financeiro', 'admin')
def guia():
    return render_template('guides/guide.html')

# Essa rota é utilizada somente pelo fluxo interno
@guide_bp.route('/emitir_guia', methods=['GET', 'POST'])
def emitir_guia():
    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        profissional_id = request.form.get('profissional_id')

        if not cliente_id or not profissional_id:
            flash('Erro: Cliente e profissional são obrigatórios!', 'danger')
            return redirect(url_for('guide_bp.emitir_guia'))
        
        agora = datetime.now()
        valor_unitario = converter_para_float(request.form.get('valor_unitario'))
        valor_total = converter_para_float(request.form.get('valor_total'))
        
        guia = Guia(
            cliente_id=cliente_id,
            profissional_id=profissional_id,
            data_original=agora,
            hora_emissao=agora.strftime('%H:%M:%S'),
            observacoes_gerais=request.form.get('observacoes_gerais'),
            quantidade_emissoes=request.form.get('quantidade_emissoes'),
            tipo_pagamento=request.form.get('tipo_pagamento'),
            valor_unitario=valor_unitario,
            valor_total = valor_total,
            pago = "Aprovado"
        )

        db.session.add(guia)
        db.session.commit()
        flash('Guia emitida com sucesso', 'success')
        return redirect(url_for('guide_bp.guia'))
        
    clientes = Cliente.query.all()
    profissionais = Profissional.query.all()
    return render_template('guides/form.html', clientes=clientes)

@guide_bp.route('/listar_guia', methods=['GET', 'POST'])
@login_required
@role_required('atendimento', 'financeiro', 'admin')
def listar_guia():
    guias = Guia.query.all()
    usuario = current_user
    return render_template('guides/list.html', guias = guias, usuario=usuario)

@guide_bp.route('/editar_guia/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('financeiro', 'admin')
def editar_guia(id):
    guia = Guia.query.get_or_404(id)
    clientes = Cliente.query.all()
    profissionais = Profissional.query.all()
    valor_formatado = formatar_para_moeda(guia.valor_unitario)
    valor_total = formatar_para_moeda(guia.valor_total )

    if request.method == 'POST':
        guia.client_id = request.form.get('client_id')
        guia.profissional_id = request.form.get('profissional_id')
        guia.observacoes_gerais = request.form.get('observacoes_gerais')
        guia.quantidade_emissoes = request.form.get('quantidade_emissoes')
        guia.tipo_pagamento = request.form.get('tipo_pagamento')
        guia.valor_unitario = converter_para_float(request.form.get('valor_unitario'))
        guia.valor_total = converter_para_float(request.form.get('valor_total'))

        db.session.commit()
        flash('Guia atualizada com sucessso', 'success')
        return redirect(url_for('guide_bp.guia'))
    return render_template('guides/form_edit.html', guia = guia, clientes=clientes, profissionais=profissionais, valor_formatado=valor_formatado, valor_total=valor_total)

@guide_bp.route('/deletar_guia/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def deletar_guia(id):
    guia = Guia.query.get_or_404(id)
    db.session.delete(guia)
    db.session.commit()
    flash('Guia deletada com sucesso', 'success')
    return redirect(url_for('guide_bp.listar_guia'))

@guide_bp.route("/filtrar_guia", methods=["GET", "POST"])
def filtrar_guia():
    query = request.args.get("q", "").strip()
    if query:
        guias = Guia.query.filter(Guia.id.ilike(f"%{query}%")).limit(10).all()
        return jsonify([
            {"id": c.id, "cliente": c.cliente.nome, "profissional": c.profissional.nome, "valor": formatar_para_moeda(c.valor_total)} 
            for c in guias
        ])
    return jsonify([])

@guide_bp.route('/aprovar_guia/<int:id>', methods=["GET", "POST"])
def aprovar_guia(id):
    guia = Guia.query.get_or_404(id)
    guia.pago = "Aprovado"
    db.session.commit()
    flash('Guia aprovada com sucesso')
    return redirect(url_for('guide_bp.listar_guia'))