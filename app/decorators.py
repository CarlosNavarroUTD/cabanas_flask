# app/decorators.py
from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if user is authenticated
            if not current_user.is_authenticated:
                flash('Debes iniciar sesión para acceder a esta página.', 'warning')
                return redirect(url_for('usuarios.login'))
            
            # Check if user's role is in allowed roles
            if current_user.tipo_usuario not in allowed_roles:
                flash('No tienes permisos para acceder a esta página.', 'danger')
                return redirect(url_for('home.index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return role_required(['admin'])(f)

def arrendador_required(f):
    return role_required(['arrendador', 'admin'])(f)

def cliente_required(f):
    return role_required(['cliente'])(f)
    