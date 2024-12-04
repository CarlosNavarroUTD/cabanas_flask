from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Arrendador, Actividad

actividades_bp = Blueprint('actividades', __name__)

@actividades_bp.route('/actividades')
def lista_actividades():
    actividades = Actividad.query.all()
    return render_template('actividades/lista.html', actividades=actividades)
