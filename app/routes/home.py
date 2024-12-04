from flask import Blueprint, render_template
from flask_login import login_required

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    """
    Renderiza la página de inicio de la aplicación.
    """
    return render_template('home.html')