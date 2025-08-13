from flask import Blueprint, render_template, send_file
from app.models import Encaminhamento, Cliente, Profissional
from weasyprint import HTML
import io

from app.utils.login_required import required_login

report_bp = Blueprint('report_bp', __name__)

@report_bp.route('/relatorios')
def relatorios():
 return render_template('relatorios/menu_relatorios.html')
