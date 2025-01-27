from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Profissional

professional_bp = Blueprint('professional_bp', __name__)

