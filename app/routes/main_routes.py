from flask import Blueprint, render_template, request, redirect, url_for

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
    return "<h1><strong>Aplicativo funcionando</trong></h1>"