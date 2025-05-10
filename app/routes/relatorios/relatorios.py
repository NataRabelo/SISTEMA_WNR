from flask import Blueprint, render_template, send_file
from app.models import Encaminhamento, Cliente, Profissional
from weasyprint import HTML
import io

from app.utils.login_required import required_login

report_bp = Blueprint('report_bp', __name__)


@report_bp.route('/report_cliente', methods=['GET', 'POST'])
@required_login
def report_cliente():
    clientes = Cliente.query.all()  # Altere para plural

    html_content = render_template('reports/report_cliente.html', clientes=clientes)

    pdf_io = io.BytesIO()
    HTML(string=html_content).write_pdf(pdf_io)
    pdf_io.seek(0)

    return send_file(pdf_io, as_attachment=True, download_name='clientes.pdf', mimetype='application/pdf')


@report_bp.route('/report_profissional', methods=['GET', 'POST'])
@required_login
def report_profissional():
    profissionais = Profissional.query.all()  # Altere para plural

    html_content = render_template('reports/report_profissional.html', profissionais=profissionais)

    pdf_io = io.BytesIO()
    HTML(string=html_content).write_pdf(pdf_io)
    pdf_io.seek(0)

    return send_file(pdf_io, as_attachment=True, download_name='profissionais.pdf', mimetype='application/pdf')


@report_bp.route('/report_encaminhamento', methods=['GET', 'POST'])
@required_login
def report_encaminhamento():
    encaminhamentos = Encaminhamento.query.all()  # Altere para plural

    html_content = render_template('reports/report_encaminhamento.html', encaminhamentos=encaminhamentos)

    pdf_io = io.BytesIO()
    HTML(string=html_content).write_pdf(pdf_io)
    pdf_io.seek(0)

    return send_file(pdf_io, as_attachment=True, download_name='encaminhamentos.pdf', mimetype='application/pdf')
