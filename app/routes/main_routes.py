from flask import Blueprint, render_template, request, redirect, url_for

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
    return render_template('main/index.html')

@main_bp.route('/menu')
def menu():
    return render_template('main/teste_logado.html')