from flask import Blueprint, flash, jsonify, request
from app.utils.decorators import role_required
from flask_login import login_required
from app.models import Profissional, Cliente, Encaminhamento
from app.utils.editor_valor import formatar_para_moeda

utils_bp = Blueprint('utils_bp', __name__)


@utils_bp.route('/buscar_profissional', methods=['GET'])
@login_required
@role_required('atendimento', 'financeiro', 'admin')
def buscar_profissional():
    codigo = request.args.get('codigo')
    profissional = Profissional.query.filter_by(id=codigo).first()
    if profissional:
        return jsonify({'nome': profissional.nome})
    return jsonify({'erro': 'Profissional não encontrado'}), 404


@utils_bp.route('/buscar_cliente', methods=['GET'])
@login_required
@role_required('atendimento', 'financeiro', 'admin')
def buscar_cliente():
    codigo = request.args.get('codigo')
    cliente = Cliente.query.filter_by(id=codigo).first()
    if cliente:
        return jsonify({'nome': cliente.nome})
    return jsonify({'erro': 'Cliente não encontrado'}), 404


@utils_bp.route('/buscar_profissionais/<int:cliente_id>', methods=['GET'])
def buscar_profissionais(cliente_id):
    encaminhamentos = Encaminhamento.query.filter_by(cliente_id=cliente_id).all()
    profissionais = [profissional for enc in encaminhamentos for profissional in Profissional.query.filter_by(id=enc.profissional_id).all()]

    return jsonify({
        "profissionais": [{"id": p.id, "nome": p.nome, "graduacao": p.graduacao} for p in profissionais]
    })


@utils_bp.route('/buscar_valor', methods=['GET'])
@login_required
@role_required('atendimento', 'financeiro', 'admin')
def buscar_valor():
    codCliente = request.args.get('codigoCliente')
    codProfissional = request.args.get('codigoProfissional')
    tipoPagamento = request.args.get('tipoPagamento')
    encaminhamento = Encaminhamento.query.filter_by(cliente_id=codCliente, profissional_id=codProfissional).first()
    if encaminhamento:

        valor = float(encaminhamento.valor)

        if tipoPagamento == "Cartão de Crédito":
            return jsonify({'valor':formatar_para_moeda( valor + 2.0)})
        else:
            return jsonify({'valor': formatar_para_moeda(valor)})
    return jsonify({'erro': 'Valor não encontrado'}), 404