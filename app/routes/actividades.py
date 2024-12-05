from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Actividad, Arrendador, ImagenActividad
import os
from werkzeug.utils import secure_filename
from app.decorators import arrendador_required

actividades_bp = Blueprint('actividades', __name__)

@actividades_bp.route('/actividades')
def lista_actividades():
    actividades = Actividad.query.all()
    return render_template('actividades/lista.html', actividades=actividades)

@actividades_bp.route('/actividades/crear', methods=['GET', 'POST'])
@login_required
@arrendador_required
def crear_actividad():
    # Ensure only arrendadores can create actividades
    if current_user.tipo_usuario not in ['arrendador', 'admin']:
        flash('No tienes permiso para crear actividades', 'error')
        return redirect(url_for('actividades.lista_actividades'))
    
    # Find the arrendador associated with the current user
    arrendador = Arrendador.query.filter_by(usuario_id=current_user.id).first()
    
    if not arrendador:
        flash('Debes ser un arrendador para crear actividades', 'error')
        return redirect(url_for('actividades.lista_actividades'))
    
    if request.method == 'POST':
        # Create new actividad
        nueva_actividad = Actividad(
            arrendador_id=arrendador.id_arrendador,
            nombre=request.form['nombre'],
            descripcion=request.form['descripcion'],
            costo=float(request.form['costo'])
        )
        
        try:
            db.session.add(nueva_actividad)
            db.session.flush()  # Get the ID before committing
            
            # Handle image uploads
            imagenes = request.files.getlist('imagenes')
            for i, imagen in enumerate(imagenes):
                if imagen:
                    filename = secure_filename(imagen.filename)
                    filepath = os.path.join('app/static/uploads/actividades', filename)
                    imagen.save(filepath)
                    
                    # Create image record
                    imagen_actividad = ImagenActividad(
                        actividad_id=nueva_actividad.id,
                        imagen=f'/static/uploads/actividades/{filename}',
                        es_principal=(i == 0)  # First image is principal
                    )
                    db.session.add(imagen_actividad)
            
            db.session.commit()
            flash('Actividad creada exitosamente', 'success')
            return redirect(url_for('actividades.lista_actividades'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear actividad: {str(e)}', 'error')
    
    return render_template('actividades/form.html')

@actividades_bp.route('/actividades/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_actividad(id):
    actividad = Actividad.query.get_or_404(id)
    
    # Check permissions
    if current_user.tipo_usuario not in ['admin'] and actividad.arrendador_id != current_user.arrendador.id_arrendador:
        flash('No tienes permiso para editar esta actividad', 'error')
        return redirect(url_for('actividades.lista_actividades'))
    
    if request.method == 'POST':
        # Update actividad details
        actividad.nombre = request.form['nombre']
        actividad.descripcion = request.form['descripcion']
        actividad.costo = float(request.form['costo'])
        
        try:
            # Handle image uploads
            imagenes = request.files.getlist('imagenes')
            if imagenes and imagenes[0].filename:
                # Remove existing images
                ImagenActividad.query.filter_by(actividad_id=actividad.id).delete()
                
                for i, imagen in enumerate(imagenes):
                    filename = secure_filename(imagen.filename)
                    filepath = os.path.join('app/static/uploads/actividades', filename)
                    imagen.save(filepath)
                    
                    # Create image record
                    imagen_actividad = ImagenActividad(
                        actividad_id=actividad.id,
                        imagen=f'/static/uploads/actividades/{filename}',
                        es_principal=(i == 0)  # First image is principal
                    )
                    db.session.add(imagen_actividad)
            
            db.session.commit()
            flash('Actividad actualizada exitosamente', 'success')
            return redirect(url_for('actividades.lista_actividades'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar actividad: {str(e)}', 'error')
    
    return render_template('actividades/form.html', actividad=actividad)
    
@actividades_bp.route('/actividades/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_actividad(id):
    actividad = Actividad.query.get_or_404(id)
    
    # Check permissions
    if current_user.tipo_usuario not in ['admin'] and actividad.arrendador_id != current_user.arrendador.id_arrendador:
        flash('No tienes permiso para eliminar esta actividad', 'error')
        return redirect(url_for('actividades.lista_actividades'))
    
    try:
        # Remove associated images first
        ImagenActividad.query.filter_by(actividad_id=actividad.id).delete()
        
        db.session.delete(actividad)
        db.session.commit()
        flash('Actividad eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar actividad: {str(e)}', 'error')
    
    return redirect(url_for('actividades.lista_actividades'))