from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Cliente

client_bp = Blueprint('client_bp', __name__)
