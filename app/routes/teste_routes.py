from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app.utils.decorators import role_required

teste_bp = Blueprint('teste_bp', __name__)

@teste_bp.route('/nivel1')
@login_required
@role_required('user', 'supervisor', 'admin')  # Todos podem acessar
def nivel1():
    return "Bem vindo ao acesso de nível 1"

@teste_bp.route('/nivel2')
@login_required
@role_required('supervisor', 'admin')  # Supervisor e admin podem acessar
def nivel2():
    return "Bem vindo ao acesso de nível 2"

@teste_bp.route('/nivel3')
@login_required
@role_required('admin')  # Apenas admin pode acessar
def nivel3():
    return "Bem vindo ao acesso de nível 3"
