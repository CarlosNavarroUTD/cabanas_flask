from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Amenidad, ImagenAmenidad
import os
from werkzeug.utils import secure_filename
from app.decorators import arrendador_required, admin_required
from flask import jsonify

# Crear el Blueprint para amenidades
amenidades_bp = Blueprint('amenidades', __name__)

# Validar extensiones de imágenes permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@amenidades_bp.route('/api/amenidades', methods=['GET'])
def obtener_amenidades_json():
    """Devuelve todas las amenidades en formato JSON."""
    try:
        amenidades = Amenidad.query.all()
        # Serializamos las amenidades
        amenidades_serializadas = [
            {"id": amenidad.id, "nombre": amenidad.nombre}
            for amenidad in amenidades
        ]
        return jsonify(amenidades_serializadas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@amenidades_bp.route('/amenidades')
def lista_amenidades():
    """Lista todas las amenidades disponibles."""
    amenidades = Amenidad.query.all()
    return render_template('amenidades/lista.html', amenidades=amenidades)

@amenidades_bp.route('/amenidades/crear', methods=['GET', 'POST'])
@arrendador_required
def crear_amenidad():
    """Permite a los arrendadores y administradores crear una nueva amenidad."""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        
        nueva_amenidad = Amenidad(nombre=nombre, descripcion=descripcion)
        
        try:
            db.session.add(nueva_amenidad)
            db.session.flush()  # Obtener el ID antes del commit
            
            # Manejar imágenes subidas
            imagenes = request.files.getlist('imagenes')
            for imagen in imagenes:
                if imagen and allowed_file(imagen.filename):
                    filename = secure_filename(imagen.filename)
                    filepath = os.path.join('app/static/uploads/amenidades', filename)
                    imagen.save(filepath)
                    
                    imagen_amenidad = ImagenAmenidad(
                        amenidad_id=nueva_amenidad.id,
                        imagen=f'/static/uploads/amenidades/{filename}'
                    )
                    db.session.add(imagen_amenidad)
            
            db.session.commit()
            flash('Amenidad creada exitosamente', 'success')
            return redirect(url_for('amenidades.lista_amenidades'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear amenidad: {str(e)}', 'error')
    
    return render_template('amenidades/form.html')

@amenidades_bp.route('/amenidades/editar/<int:id>', methods=['GET', 'POST'])
@arrendador_required
def editar_amenidad(id):
    """Permite a los administradores editar una amenidad existente."""
    amenidad = Amenidad.query.get_or_404(id)
    
    if request.method == 'POST':
        amenidad.nombre = request.form.get('nombre')
        amenidad.descripcion = request.form.get('descripcion')
        
        try:
            imagenes = request.files.getlist('imagenes')
            if imagenes and imagenes[0].filename:
                ImagenAmenidad.query.filter_by(amenidad_id=amenidad.id).delete()
                
                for imagen in imagenes:
                    if imagen and allowed_file(imagen.filename):
                        filename = secure_filename(imagen.filename)
                        filepath = os.path.join('app/static/uploads/amenidades', filename)
                        imagen.save(filepath)
                        
                        imagen_amenidad = ImagenAmenidad(
                            amenidad_id=amenidad.id,
                            imagen=f'/static/uploads/amenidades/{filename}'
                        )
                        db.session.add(imagen_amenidad)
            
            db.session.commit()
            flash('Amenidad actualizada exitosamente', 'success')
            return redirect(url_for('amenidades.lista_amenidades'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar amenidad: {str(e)}', 'error')
    
    return render_template('amenidades/form.html', amenidad=amenidad)

@amenidades_bp.route('/amenidades/eliminar/<int:id>', methods=['POST'])
@arrendador_required
def eliminar_amenidad(id):
    """Permite a los administradores eliminar una amenidad existente."""
    amenidad = Amenidad.query.get_or_404(id)
    
    try:
        ImagenAmenidad.query.filter_by(amenidad_id=amenidad.id).delete()
        db.session.delete(amenidad)
        db.session.commit()
        flash('Amenidad eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar amenidad: {str(e)}', 'error')
    
    return redirect(url_for('amenidades.lista_amenidades'))
