from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Encaminhamento

Encaminhamento_bp = Blueprint('Encaminhamento_bp', __name__)

