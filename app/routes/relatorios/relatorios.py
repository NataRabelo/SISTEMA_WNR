from datetime import datetime
from flask import Blueprint, make_response, render_template, send_file
from app.models import Encaminhamento, Cliente, Profissional, Guia
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