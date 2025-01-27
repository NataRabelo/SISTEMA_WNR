from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Guia

guide_bp = Blueprint('guide_bp', __name__)

