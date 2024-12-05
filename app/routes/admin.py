# app/routes/admin.py
from flask import Blueprint, render_template
from flask_login import login_required
from app.decorators import arrendador_required
from app.models import Usuario, Cabana

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
@arrendador_required
def dashboard():
    total_users = Usuario.query.count()
    total_cabanas = Cabana.query.count()

    return render_template('admin/dashboard.html', 
                           total_users=total_users, 
                           total_cabanas=total_cabanas)

@admin_bp.route('/usuarios')
@login_required
@arrendador_required
def usuarios():
    usuarios = Usuario.query.all()
    return render_template('admin/usuarios.html', usuarios=usuarios)