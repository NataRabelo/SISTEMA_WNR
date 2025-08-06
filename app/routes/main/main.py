from user_agents import parse
from flask import Blueprint, render_template, request, abort
from flask_login import current_user
from app.utils.login_required import required_login

main_bp = Blueprint('main_bp', __name__)

@main_bp.before_request
def bloquear_mobile():
    user_agent_str = request.headers.get('User-Agent')
    user_agent = parse(user_agent_str)

    if user_agent.is_mobile:
        return abort(403, description="Acesso via mobile não permitido.")

@main_bp.route('/')
def index():
    return render_template('main/index.html')


@main_bp.route('/menu')
@required_login
def menu():
    usuario = current_user
    return render_template('main/menu.html', usuario=usuario)
