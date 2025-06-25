from datetime import datetime
from flask import Blueprint, flash, jsonify, render_template, request, redirect, url_for
from flask_login import current_user
from app.models import Cliente, MetodoPagamento, Guia, Profissional
from app import db
from app.utils.decorators import role_required
from app.utils.editor_valor import converter_para_float, formatar_para_moeda
from app.utils.login_required import required_login

guide_bp = Blueprint('guide_bp', __name__)


@guide_bp.route('/guia', methods=['GET', 'POST'])
@required_login
@role_required('atendimento', 'financeiro', 'admin')
def guia():
    return render_template('guia/guide.html')

# Essa rota é utilizada somente pelo fluxo interno


@guide_bp.route('/emitir_guia', methods=['GET', 'POST'])
def emitir_guia():

    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        profissional_id = request.form.get('profissional_id')
        usuario = current_user

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
            metodo_pagamento_id=int(request.form.get('tipo_pagamento')),
            valor_unitario=valor_unitario,
            valor_total=valor_total,
            pago="Aprovada",
            usuario_emitente_id=usuario.id
        )

        db.session.add(guia)
        db.session.commit()
        flash('Guia emitida com sucesso', 'success')
        return redirect(url_for('guide_bp.guia'))

    clientes = Cliente.query.all()
    pagamentos = MetodoPagamento.query.all()
    return render_template('guia/form.html',
                           clientes=clientes,
                           pagamentos=pagamentos)


@guide_bp.route('/listar_guia', methods=['GET', 'POST'])
@required_login
@role_required('atendimento', 'financeiro', 'admin')
def listar_guia():
    guias = Guia.query.all()
    usuario = current_user
    return render_template('guia/list.html', guias=guias, usuario=usuario)


@guide_bp.route('/editar_guia/<int:id>', methods=['GET', 'POST'])
@required_login
@role_required('financeiro', 'admin')
def editar_guia(id):
    guia = Guia.query.get_or_404(id)
    clientes = Cliente.query.all()
    profissionais = Profissional.query.all()
    valor_formatado = formatar_para_moeda(guia.valor_unitario)
    valor_total = formatar_para_moeda(guia.valor_total)

    if request.method == 'POST':
        guia.client_id = request.form.get('client_id')
        guia.profissional_id = request.form.get('profissional_id')
        guia.observacoes_gerais = request.form.get('observacoes_gerais')
        guia.quantidade_emissoes = request.form.get('quantidade_emissoes')
        guia.metodo_pagamento_id = int(request.form.get('tipo_pagamento'))
        guia.valor_unitario = converter_para_float(request.form.get('valor_unitario'))
        guia.valor_total = converter_para_float(request.form.get('valor_total'))

        db.session.commit()
        flash('Guia atualizada com sucessso', 'success')
        return redirect(url_for('guide_bp.guia'))
    pagamentos = MetodoPagamento.query.all()
    return render_template('guia/form_edit.html',
                           guia=guia,
                           clientes=clientes,
                           profissionais=profissionais,
                           valor_formatado=valor_formatado,
                           valor_total=valor_total,
                           pagamentos=pagamentos)


@guide_bp.route('/deletar_guia/<int:id>', methods=['GET', 'POST'])
@required_login
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
            {"id": c.id,
             "cliente": c.cliente.nome,
             "profissional": c.profissional.nome,
             "valor": formatar_para_moeda(c.valor_total)}
            for c in guias
        ])
    return jsonify([])


@guide_bp.route('/aprovar_guia/<int:id>', methods=["GET", "POST"])
def aprovar_guia(id):
    guia = Guia.query.get_or_404(id)
    guia.pago = "Aprovada"
    db.session.commit()
    return redirect(url_for('guide_bp.listar_guia'))


@guide_bp.route('/reprovar_guia/<int:id>', methods=["GET", "POST"])
def reprovar_guia(id):
    guia = Guia.query.get_or_404(id)
    guia.pago = "Pendente"
    db.session.commit()
    return redirect(url_for('guide_bp.listar_guia'))
