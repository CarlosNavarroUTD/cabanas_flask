# app/routes/usuarios.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import Usuario, Arrendador, Cliente
from app.decorators import role_required

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and usuario.check_password(password):
            login_user(usuario)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('home.index'))
        
        flash('Correo o contraseña inválidos', 'error')
    
    return render_template('usuarios/login.html')

@usuarios_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('home.index'))

@usuarios_bp.route('/register', methods=['GET', 'POST'])
@usuarios_bp.route('/register/<user_type>', methods=['GET', 'POST'])
def register(user_type='cliente'):
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    
    # Get user_type from form if not in URL
    if request.method == 'POST':
        user_type = request.form.get('tipo_usuario', user_type)
    
    if user_type not in ['cliente', 'arrendador']:
        flash('Tipo de usuario inválido', 'error')
        return redirect(url_for('home.index'))
    
    if request.method == 'POST':
        nombre_usuario = request.form.get('nombre_usuario')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if user already exists
        if Usuario.query.filter_by(email=email).first():
            flash('El correo electrónico ya está registrado', 'error')
            return redirect(url_for('usuarios.register', user_type=user_type))
        
        # Create new user
        nuevo_usuario = Usuario(
            nombre_usuario=nombre_usuario, 
            email=email,
            tipo_usuario=user_type
        )
        nuevo_usuario.set_password(password)
        
        db.session.add(nuevo_usuario)
        db.session.flush()  # This will generate the id without committing
        
        # Create corresponding Arrendador or Cliente record
        if user_type == 'arrendador':
            nuevo_arrendador = Arrendador(
                nombre=nuevo_usuario.nombre_usuario,
                usuario_id=nuevo_usuario.id
            )
            db.session.add(nuevo_arrendador)
        else:  # cliente
            nuevo_cliente = Cliente(
                usuario_id=nuevo_usuario.id
            )
            db.session.add(nuevo_cliente)
        
        db.session.commit()
        
        flash('Registro exitoso. Por favor inicia sesión.', 'success')
        return redirect(url_for('usuarios.login'))
    
    template = f'usuarios/registro_{user_type}.html'
    return render_template(template)