from flask import Blueprint, make_response, render_template, send_file
from app.models import Encaminhamento, Cliente, Profissional
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
    html = render_template('pdf/clientes.html', clientes=clientes)

    pdf_io = io.BytesIO()
    HTML(string=html).write_pdf(pdf_io)
    pdf_io.seek(0)

    response = make_response(pdf_io.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=Relatório de clientes.pdf'
    return response