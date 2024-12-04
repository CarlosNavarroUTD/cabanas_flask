from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Cabana, Arrendador

cabanas_bp = Blueprint('cabanas', __name__)

@cabanas_bp.route('/cabanas')
def lista_cabanas():
    cabanas = Cabana.query.all()
    return render_template('cabanas/lista.html', cabanas=cabanas)

@cabanas_bp.route('/cabanas/crear', methods=['GET', 'POST'])
@login_required
def crear_cabana():
    # Ensure only arrendadores can create cabañas
    if current_user.tipo_usuario not in ['arrendador', 'admin']:
        flash('No tienes permiso para crear cabañas', 'error')
        return redirect(url_for('cabanas.lista_cabanas'))
    
    # Find the arrendador associated with the current user
    arrendador = Arrendador.query.filter_by(usuario_id=current_user.id).first()
    
    if not arrendador:
        flash('Debes ser un arrendador para crear cabañas', 'error')
        return redirect(url_for('cabanas.lista_cabanas'))
    
    if request.method == 'POST':
        # Create new cabaña
        nueva_cabana = Cabana(
            nombre=request.form['nombre'],
            descripcion=request.form['descripcion'],
            capacidad=int(request.form['capacidad']),
            costo_por_noche=float(request.form['costo_por_noche']),
            ubicacion=request.form['ubicacion'],
            arrendador_id=arrendador.id_arrendador,
            estado='disponible'  # Default state
        )
        
        try:
            db.session.add(nueva_cabana)
            db.session.commit()
            flash('Cabaña creada exitosamente', 'success')
            return redirect(url_for('cabanas.lista_cabanas'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear cabaña: {str(e)}', 'error')
    
    return render_template('cabanas/form.html')

@cabanas_bp.route('/cabanas/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_cabana(id):
    cabana = Cabana.query.get_or_404(id)
    
    # Check permissions
    if current_user.tipo_usuario not in ['admin'] and cabana.arrendador_id != current_user.arrendador.id_arrendador:
        flash('No tienes permiso para editar esta cabaña', 'error')
        return redirect(url_for('cabanas.lista_cabanas'))
    
    if request.method == 'POST':
        # Update cabaña details
        cabana.nombre = request.form['nombre']
        cabana.descripcion = request.form['descripcion']
        cabana.capacidad = int(request.form['capacidad'])
        cabana.costo_por_noche = float(request.form['costo_por_noche'])
        cabana.ubicacion = request.form['ubicacion']  # Add this line
        
        try:
            db.session.commit()
            flash('Cabaña actualizada exitosamente', 'success')
            return redirect(url_for('cabanas.lista_cabanas'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar cabaña: {str(e)}', 'error')
    
    return render_template('cabanas/form.html', cabana=cabana)
    
@cabanas_bp.route('/cabanas/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_cabana(id):
    cabana = Cabana.query.get_or_404(id)
    
    # Check permissions
    if current_user.tipo_usuario not in ['admin'] and cabana.arrendador_id != current_user.arrendador.id_arrendador:
        flash('No tienes permiso para eliminar esta cabaña', 'error')
        return redirect(url_for('cabanas.lista_cabanas'))
    
    try:
        db.session.delete(cabana)
        db.session.commit()
        flash('Cabaña eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar cabaña: {str(e)}', 'error')
    
    return redirect(url_for('cabanas.lista_cabanas'))