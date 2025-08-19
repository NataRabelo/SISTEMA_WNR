from datetime import datetime
from flask import Blueprint, make_response, render_template, request, send_file
from app.models import Encaminhamento, Cliente, Profissional, Guia
from app import db
from flask_login import current_user
from weasyprint import HTML
import io

from app.utils.login_required import required_login

report_bp = Blueprint('report_bp', __name__)

# Rota para o menu de relatórios do sistema 
@report_bp.route('/relatorios')
@required_login
def relatorios():
 return render_template('relatorios/menu_relatorios.html')

# Rota para gerar o relatório geral dos clientes cadastrados 
@report_bp.route('/relatorios/clientes')
@required_login
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

# Rota para gerar o relatório geral dos profissionais cadastrados
@report_bp.route('/relatorios/profissionais')
@required_login
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

# Rota para gerar o relatório geral dos encaminhamentos realizados 
@report_bp.route('/relatorios/encaminhamentos')
@required_login
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

# Rota para gerar o relatório geral das guias emitidas 
@report_bp.route('/relatorios/guias')
@required_login
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

# Rota para gerar o relatório de guias emitidas em uma data específica 
@report_bp.route('/relatorios/guias_do_dia')
@required_login
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

# Rota para gerar guias emitidas para cada profissional em um período
@report_bp.route('/relatorios/guias_por_profissional')
@required_login
def visualizar_guias_por_profissional_pdf():
    data_inicio_str = request.args.get("data_inicio")
    data_fim_str = request.args.get("data_fim")

    try:
        if data_inicio_str and data_fim_str:
            data_inicio = datetime.strptime(data_inicio_str, "%Y-%m-%d").date()
            data_fim = datetime.strptime(data_fim_str, "%Y-%m-%d").date()

            guias = Guia.query.filter(
                db.func.date(Guia.data_original).between(data_inicio, data_fim)
            ).all()
            periodo = f"{data_inicio.strftime('%d/%m/%Y')} até {data_fim.strftime('%d/%m/%Y')}"
        else:
            # Caso não passe parâmetros, pega todas
            guias = Guia.query.all()
            periodo = "Todas as datas"
    except ValueError:
        return "Datas inválidas. Use o formato YYYY-MM-DD", 400

    # ==== ORGANIZAR POR PROFISSIONAL ====
    guias_por_profissional = {}
    totais_profissionais = {}
    total_geral = 0

    for guia in guias:
        profissional = guia.profissional.nome if guia.profissional else "Não informado"
        valor = guia.valor_total or 0

        if profissional not in guias_por_profissional:
            guias_por_profissional[profissional] = []
            totais_profissionais[profissional] = 0

        guias_por_profissional[profissional].append(guia)
        totais_profissionais[profissional] += valor
        total_geral += valor

    # Data do relatório
    data_atual = datetime.now().strftime('%d/%m/%Y')

    # Renderizar o template
    html = render_template(
        'pdf/guias_por_profissional.html',
        guias_por_profissional=guias_por_profissional,
        totais_profissionais=totais_profissionais,
        total_geral=total_geral,
        data_atual=data_atual,
        periodo=periodo
    )

    # Gerar PDF
    pdf_io = io.BytesIO()
    HTML(string=html).write_pdf(pdf_io)
    pdf_io.seek(0)

    response = make_response(pdf_io.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=Relatorio_guias_por_profissional.pdf'
    return response
