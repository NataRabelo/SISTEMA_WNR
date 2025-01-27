from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Usuario

auth_bp = Blueprint('auth_bp', __name__)
