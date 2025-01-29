from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
    return render_template('main/index.html')


@main_bp.route('/menu')
@login_required
def menu():
    return render_template('main/menu.html')