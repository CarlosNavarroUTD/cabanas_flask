"""empty message

Revision ID: 8999b4d97ee3
Revises: 
Create Date: 2024-12-04 13:12:01.341447

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8999b4d97ee3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_usuario', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=254), nullable=False),
    sa.Column('nombre_usuario', sa.String(length=255), nullable=False),
    sa.Column('tipo_usuario', sa.Enum('cliente', 'arrendador', 'admin', name='tipo_usuario_enum'), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id_usuario'),
    sa.UniqueConstraint('nombre_usuario')
    )
    op.create_table('Arrendador',
    sa.Column('id_arrendador', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=255), nullable=True),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['usuario_id'], ['Usuario.id'], ),
    sa.PrimaryKeyConstraint('id_arrendador'),
    sa.UniqueConstraint('usuario_id')
    )
    op.create_table('Cliente',
    sa.Column('id_cliente', sa.Integer(), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['usuario_id'], ['Usuario.id'], ),
    sa.PrimaryKeyConstraint('id_cliente'),
    sa.UniqueConstraint('usuario_id')
    )
    op.create_table('Actividad',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('arrendador_id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=255), nullable=False),
    sa.Column('descripcion', sa.Text(), nullable=False),
    sa.Column('costo', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['arrendador_id'], ['Arrendador.id_arrendador'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Cabana',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=255), nullable=False),
    sa.Column('descripcion', sa.Text(), nullable=False),
    sa.Column('capacidad', sa.Integer(), nullable=False),
    sa.Column('costo_por_noche', sa.Float(), nullable=False),
    sa.Column('estado', sa.Enum('disponible', 'ocupada', 'mantenimiento', 'inactiva', name='cabana_estado_enum'), nullable=True),
    sa.Column('arrendador_id', sa.Integer(), nullable=False),
    sa.Column('ubicacion_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['arrendador_id'], ['Arrendador.id_arrendador'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Paquete',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('arrendador_id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=255), nullable=False),
    sa.Column('noches', sa.Integer(), nullable=True),
    sa.Column('precio_base', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['arrendador_id'], ['Arrendador.id_arrendador'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ImagenCabana',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cabana_id', sa.Integer(), nullable=False),
    sa.Column('imagen', sa.String(length=255), nullable=False),
    sa.Column('es_principal', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['cabana_id'], ['Cabana.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('PaqueteActividad',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('paquete_id', sa.Integer(), nullable=False),
    sa.Column('actividad_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['actividad_id'], ['Actividad.id'], ),
    sa.ForeignKeyConstraint(['paquete_id'], ['Paquete.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('PaqueteCabana',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('paquete_id', sa.Integer(), nullable=False),
    sa.Column('cabana_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cabana_id'], ['Cabana.id'], ),
    sa.ForeignKeyConstraint(['paquete_id'], ['Paquete.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Resena',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cabana_id', sa.Integer(), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('calificacion', sa.Integer(), nullable=False),
    sa.Column('comentario', sa.Text(), nullable=True),
    sa.Column('fecha_creacion', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['cabana_id'], ['Cabana.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['Usuario.id_usuario'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Resena')
    op.drop_table('PaqueteCabana')
    op.drop_table('PaqueteActividad')
    op.drop_table('ImagenCabana')
    op.drop_table('Paquete')
    op.drop_table('Cabana')
    op.drop_table('Actividad')
    op.drop_table('Cliente')
    op.drop_table('Arrendador')
    op.drop_table('Usuario')
    # ### end Alembic commands ###