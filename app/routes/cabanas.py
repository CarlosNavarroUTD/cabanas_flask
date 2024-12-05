from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Cabana, Amenidad, CabanaAmenidad, ImagenCabana
from app.decorators import arrendador_required
import os
from werkzeug.utils import secure_filename

# Crear el Blueprint para cabañas
cabanas_bp = Blueprint('cabanas', __name__)

# Validar extensiones de imágenes permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@cabanas_bp.route('/cabanas')
def lista_cabanas():
    """Lista todas las cabañas disponibles."""
    cabanas = Cabana.query.all()
    return render_template('cabanas/lista.html', cabanas=cabanas)

@cabanas_bp.route('/cabanas/crear', methods=['GET', 'POST'])
@arrendador_required
def crear_cabana():
    """Permite a los arrendadores crear una nueva cabaña."""
    amenidades = Amenidad.query.all()
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        capacidad = request.form.get('capacidad')
        costo_por_noche = request.form.get('costo_por_noche')
        ubicacion = request.form.get('ubicacion')
        estado = request.form.get('estado', 'disponible')
        amenidades_seleccionadas = request.form.getlist('amenidades')
        
        # Obtener el ID del arrendador actual (asumiendo que hay un método para obtenerlo)
        arrendador_id = current_user.arrendador.id_arrendador
        
        nueva_cabana = Cabana(
            nombre=nombre, 
            descripcion=descripcion, 
            capacidad=int(capacidad),
            costo_por_noche=float(costo_por_noche),
            ubicacion=ubicacion,
            estado=estado,
            arrendador_id=arrendador_id
        )
        
        try:
            db.session.add(nueva_cabana)
            db.session.flush()  # Obtener el ID antes del commit
            
            # Asociar amenidades seleccionadas
            for amenidad_id in amenidades_seleccionadas:
                cabana_amenidad = CabanaAmenidad(
                    cabana_id=nueva_cabana.id,
                    amenidad_id=int(amenidad_id)
                )
                db.session.add(cabana_amenidad)
            
            # Manejar imágenes subidas
            imagenes = request.files.getlist('imagenes')
            imagen_principal = request.form.get('imagen_principal')
            
            for i, imagen in enumerate(imagenes):
                if imagen and allowed_file(imagen.filename):
                    filename = secure_filename(imagen.filename)
                    filepath = os.path.join('app/static/uploads/cabanas', filename)
                    imagen.save(filepath)
                    
                    imagen_cabana = ImagenCabana(
                        cabana_id=nueva_cabana.id,
                        imagen=f'/static/uploads/cabanas/{filename}',
                        es_principal=(imagen_principal == str(i))
                    )
                    db.session.add(imagen_cabana)
            
            db.session.commit()
            flash('Cabaña creada exitosamente', 'success')
            return redirect(url_for('cabanas.lista_cabanas'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear cabaña: {str(e)}', 'error')
    
    return render_template('cabanas/form.html', amenidades=amenidades)

@cabanas_bp.route('/cabanas/editar/<int:id>', methods=['GET', 'POST'])
@arrendador_required
def editar_cabana(id):
    """Permite a los arrendadores editar una cabaña existente."""
    cabana = Cabana.query.get_or_404(id)
    amenidades = Amenidad.query.all()
    
    if request.method == 'POST':
        cabana.nombre = request.form.get('nombre')
        cabana.descripcion = request.form.get('descripcion')
        cabana.capacidad = int(request.form.get('capacidad'))
        cabana.costo_por_noche = float(request.form.get('costo_por_noche'))
        cabana.ubicacion = request.form.get('ubicacion')
        cabana.estado = request.form.get('estado', 'disponible')
        
        try:
            # Eliminar amenidades existentes
            CabanaAmenidad.query.filter_by(cabana_id=cabana.id).delete()
            
            # Asociar nuevas amenidades
            amenidades_seleccionadas = request.form.getlist('amenidades')
            for amenidad_id in amenidades_seleccionadas:
                cabana_amenidad = CabanaAmenidad(
                    cabana_id=cabana.id,
                    amenidad_id=int(amenidad_id)
                )
                db.session.add(cabana_amenidad)
            
            # Manejar imágenes
            imagenes = request.files.getlist('imagenes')
            imagen_principal = request.form.get('imagen_principal')
            
            # Eliminar imágenes existentes si se suben nuevas
            if imagenes and imagenes[0].filename:
                ImagenCabana.query.filter_by(cabana_id=cabana.id).delete()
                
                for i, imagen in enumerate(imagenes):
                    if imagen and allowed_file(imagen.filename):
                        filename = secure_filename(imagen.filename)
                        filepath = os.path.join('app/static/uploads/cabanas', filename)
                        imagen.save(filepath)
                        
                        imagen_cabana = ImagenCabana(
                            cabana_id=cabana.id,
                            imagen=f'/static/uploads/cabanas/{filename}',
                            es_principal=(imagen_principal == str(i))
                        )
                        db.session.add(imagen_cabana)
            
            db.session.commit()
            flash('Cabaña actualizada exitosamente', 'success')
            return redirect(url_for('cabanas.lista_cabanas'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar cabaña: {str(e)}', 'error')
    
    return render_template('cabanas/form.html', cabana=cabana, amenidades=amenidades)

@cabanas_bp.route('/cabanas/eliminar/<int:id>', methods=['POST'])
@arrendador_required
def eliminar_cabana(id):
    """Permite a los arrendadores eliminar una cabaña existente."""
    cabana = Cabana.query.get_or_404(id)
    
    try:
        # Eliminar imágenes e información de amenidades asociadas
        ImagenCabana.query.filter_by(cabana_id=cabana.id).delete()
        CabanaAmenidad.query.filter_by(cabana_id=cabana.id).delete()
        
        db.session.delete(cabana)
        db.session.commit()
        flash('Cabaña eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar cabaña: {str(e)}', 'error')
    
    return redirect(url_for('cabanas.lista_cabanas'))