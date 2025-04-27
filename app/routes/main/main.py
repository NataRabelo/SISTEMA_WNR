from flask import Blueprint, render_template
from flask_login import current_user, login_required

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
    return render_template('main/index.html')

@main_bp.route('/menu')
@login_required
def menu():
    usuario = current_user
    return render_template('main/menu.html', usuario=usuario)