from datetime import datetime
from flask import Blueprint, make_response, render_template, request, send_file
from app.models import Encaminhamento, Cliente, Profissional, Guia
from app import db
from flask_login import current_user
from weasyprint import HTML
import io

from app.utils.login_required import required_login

report_bp = Blueprint('report_bp', __name__)

@report_bp.route('/relatorios')
def relatorios():
 return render_template('relatorios/menu_relatorios.html')


@report_bp.route('/relatorios/clientes')
def visualizar_clientes_pdf():
    clientes = Cliente.query.all()
    data_atual = datetime.now().strftime('%d/%m/%Y')
    html = render_template('pdf/clientes.html', clientes=clientes, data_atual=data_atual)

    pdf_io = io.BytesIO()
    HTML(string=html).write_pdf(pdf_io)
    pdf_io.seek(0)

    response = make_response(pdf_io.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=Relatório de clientes.pdf'
    return response

@report_bp.route('/relatorios/profissionais')
def visualizar_profissionais_pdf():
    profissionais = Profissional.query.all()
    data_atual = datetime.now().strftime('%d/%m/%Y')
    html = render_template('pdf/profissionais.html', profissionais=profissionais, data_atual=data_atual)

    pdf_io = io.BytesIO()
    HTML(string=html).write_pdf(pdf_io)
    pdf_io.seek(0)

    response = make_response(pdf_io.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=Relatório de profissionais.pdf'
    return response

@report_bp.route('/relatorios/encaminhamentos')
def visualizar_encaminhamentos_pdf():
    encaminhamentos = Encaminhamento.query.all()
    data_atual = datetime.now().strftime('%d/%m/%Y')
    html = render_template('pdf/encaminhamentos.html', encaminhamentos=encaminhamentos, data_atual=data_atual)

    pdf_io = io.BytesIO()
    HTML(string=html).write_pdf(pdf_io)
    pdf_io.seek(0)

    response = make_response(pdf_io.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=Relatório de encaminhamentos.pdf'
    return response

@report_bp.route('/relatorios/guias')
def visualizar_guias_pdf():
    guias = Guia.query.all()
    data_atual = datetime.now().strftime('%d/%m/%Y')
    html = render_template('pdf/guias.html', guias=guias, data_atual=data_atual)

    pdf_io = io.BytesIO()
    HTML(string=html).write_pdf(pdf_io)
    pdf_io.seek(0)

    response = make_response(pdf_io.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=Relatório de guias.pdf'
    return response


@report_bp.route('/relatorios/guias_do_dia')
def visualizar_guias_do_dia_pdf():
    data_str = request.args.get("data")

    if data_str:
        try:
            data_filtro = datetime.strptime(data_str, "%Y-%m-%d").date()
            guias = Guia.query.filter(db.func.date(Guia.data_original) == data_filtro).all()
            data_selecionada = data_filtro.strftime('%d/%m/%Y')
        except ValueError:
            return "Data inválida. Use o formato YYYY-MM-DD", 400
    else:
        guias = Guia.query.all()
        data_selecionada = "Todas as datas"

    # ==== TOTALIZADORES ====
    total_por_pagamento = {}
    total_geral = 0

    for guia in guias:
        metodo = guia.metodo_pagamento.nome if guia.metodo_pagamento else "Não informado"
        valor = guia.valor_total or 0

        total_por_pagamento[metodo] = total_por_pagamento.get(metodo, 0) + valor
        total_geral += valor

    data_atual = datetime.now().strftime('%d/%m/%Y')
    html = render_template(
        'pdf/guias_do_dia.html',
        guias=guias,
        data_atual=data_atual,
        data_selecionada=data_selecionada,
        total_por_pagamento=total_por_pagamento,
        total_geral=total_geral
    )

    pdf_io = io.BytesIO()
    HTML(string=html).write_pdf(pdf_io)
    pdf_io.seek(0)

    response = make_response(pdf_io.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=Relatorio_de_guias.pdf'
    return response
