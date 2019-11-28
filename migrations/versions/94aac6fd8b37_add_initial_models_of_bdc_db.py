"""Add initial models of bdc-db

Revision ID: 94aac6fd8b37
Revises:
Create Date: 2019-11-28 11:08:18.691423

"""
from alembic import op
import geoalchemy2
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94aac6fd8b37'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('grs_schemas',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('description', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('raster_chunk_schemas',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('raster_size_x', sa.Integer(), nullable=True),
    sa.Column('raster_size_y', sa.Integer(), nullable=True),
    sa.Column('raster_size_t', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('spatial_resolution_schemas',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('resolution_x', sa.Float(precision=53), nullable=False),
    sa.Column('resolution_y', sa.Float(precision=53), nullable=False),
    sa.Column('resolution_unit', sa.String(length=16), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('temporal_composition_schemas',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('temporal_composite_unit', sa.String(length=16), nullable=False),
    sa.Column('temporal_schema', sa.String(length=16), nullable=False),
    sa.Column('temporal_composite_t', sa.String(length=16), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('collections',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('spatial_resolution_schema_id', sa.String(length=20), nullable=False),
    sa.Column('temporal_composition_schema_id', sa.String(length=20), nullable=False),
    sa.Column('raster_chunk_schema_id', sa.String(length=20), nullable=False),
    sa.Column('grs_schema_id', sa.String(length=20), nullable=False),
    sa.Column('version', sa.String(length=16), nullable=False),
    sa.Column('description', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['grs_schema_id'], ['grs_schemas.id'], ),
    sa.ForeignKeyConstraint(['raster_chunk_schema_id'], ['raster_chunk_schemas.id'], ),
    sa.ForeignKeyConstraint(['spatial_resolution_schema_id'], ['spatial_resolution_schemas.id'], ),
    sa.ForeignKeyConstraint(['temporal_composition_schema_id'], ['temporal_composition_schemas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tiles',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('grs_schema_id', sa.String(length=20), nullable=False),
    sa.Column('geom_wgs84', geoalchemy2.types.Geometry(), nullable=True),
    sa.Column('geom', geoalchemy2.types.Geometry(), nullable=True),
    sa.ForeignKeyConstraint(['grs_schema_id'], ['grs_schemas.id'], ),
    sa.PrimaryKeyConstraint('id', 'grs_schema_id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_tiles_geom_wgs84'), 'tiles', ['geom_wgs84'], unique=False)
    op.create_table('asset_compositions',
    sa.Column('collection_id', sa.String(length=20), nullable=False),
    sa.Column('asset', sa.Integer(), nullable=False),
    sa.Column('scene_id', sa.String(length=64), nullable=False),
    sa.Column('description', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['collection_id'], ['collections.id'], ),
    sa.PrimaryKeyConstraint('collection_id', 'asset', 'scene_id')
    )
    op.create_table('bands',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('collection_id', sa.String(length=20), nullable=False),
    sa.Column('min', sa.Float(), nullable=True),
    sa.Column('max', sa.Float(), nullable=True),
    sa.Column('fill', sa.Integer(), nullable=True),
    sa.Column('scale', sa.String(length=16), nullable=True),
    sa.Column('common_name', sa.String(length=16), nullable=True),
    sa.Column('data_type', sa.String(length=16), nullable=True),
    sa.Column('mime_type', sa.String(length=16), nullable=True),
    sa.Column('description', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['collection_id'], ['collections.id'], ),
    sa.PrimaryKeyConstraint('id', 'collection_id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('collection_tiles',
    sa.Column('collection_id', sa.String(length=20), nullable=False),
    sa.Column('grs_schema_id', sa.String(length=20), nullable=False),
    sa.Column('tile_id', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['collection_id'], ['collections.id'], ),
    sa.ForeignKeyConstraint(['grs_schema_id'], ['grs_schemas.id'], ),
    sa.ForeignKeyConstraint(['tile_id'], ['tiles.id'], ),
    sa.PrimaryKeyConstraint('collection_id', 'grs_schema_id', 'tile_id')
    )
    op.create_table('composite_functions',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('collection_id', sa.String(length=20), nullable=False),
    sa.Column('description', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['collection_id'], ['collections.id'], ),
    sa.PrimaryKeyConstraint('id', 'collection_id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('band_compositions',
    sa.Column('collection_id', sa.String(length=20), nullable=False),
    sa.Column('band_id', sa.Integer(), nullable=False),
    sa.Column('product', sa.String(length=16), nullable=False),
    sa.Column('product_band', sa.String(length=16), nullable=False),
    sa.Column('description', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['band_id'], ['bands.id'], ),
    sa.ForeignKeyConstraint(['collection_id'], ['collections.id'], ),
    sa.PrimaryKeyConstraint('collection_id', 'band_id', 'product', 'product_band'),
    sa.UniqueConstraint('product'),
    sa.UniqueConstraint('product_band')
    )
    op.create_table('collection_items',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('collection_id', sa.String(length=20), nullable=False),
    sa.Column('grs_schema_id', sa.String(length=20), nullable=False),
    sa.Column('tile_id', sa.String(length=20), nullable=False),
    sa.Column('composite_function_id', sa.String(length=20), nullable=False),
    sa.Column('item_date', sa.Date(), nullable=False),
    sa.Column('composite_start', sa.Date(), nullable=False),
    sa.Column('composite_end', sa.Date(), nullable=True),
    sa.Column('quicklook', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['collection_id'], ['collections.id'], ),
    sa.ForeignKeyConstraint(['composite_function_id'], ['composite_functions.id'], ),
    sa.ForeignKeyConstraint(['grs_schema_id'], ['grs_schemas.id'], ),
    sa.ForeignKeyConstraint(['tile_id'], ['tiles.id'], ),
    sa.PrimaryKeyConstraint('id', 'collection_id', 'grs_schema_id', 'tile_id', 'composite_function_id', 'item_date'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_collection_items_composite_end'), 'collection_items', ['composite_end'], unique=False)
    op.create_index(op.f('ix_collection_items_composite_start'), 'collection_items', ['composite_start'], unique=False)
    op.create_table('cubes',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('collection_id', sa.String(length=20), nullable=True),
    sa.Column('composite_function_id', sa.String(length=20), nullable=True),
    sa.Column('oauth_info', sa.String(length=16), nullable=True),
    sa.Column('description', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['collection_id'], ['collections.id'], ),
    sa.ForeignKeyConstraint(['composite_function_id'], ['composite_functions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('assets',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('collection_id', sa.String(length=20), nullable=False),
    sa.Column('band_id', sa.Integer(), nullable=False),
    sa.Column('grs_schema_id', sa.String(length=20), nullable=False),
    sa.Column('tile_id', sa.String(length=20), nullable=False),
    sa.Column('composite_function_id', sa.String(length=20), nullable=True),
    sa.Column('collection_item_id', sa.String(length=64), nullable=False),
    sa.Column('url', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['band_id'], ['bands.id'], ),
    sa.ForeignKeyConstraint(['collection_id'], ['collections.id'], ),
    sa.ForeignKeyConstraint(['collection_item_id'], ['collection_items.id'], ),
    sa.ForeignKeyConstraint(['composite_function_id'], ['composite_functions.id'], ),
    sa.ForeignKeyConstraint(['grs_schema_id'], ['grs_schemas.id'], ),
    sa.ForeignKeyConstraint(['tile_id'], ['tiles.id'], ),
    sa.PrimaryKeyConstraint('id', 'collection_id', 'band_id', 'grs_schema_id', 'tile_id', 'collection_item_id')
    )
    op.create_index(op.f('ix_assets_collection_item_id'), 'assets', ['collection_item_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_assets_collection_item_id'), table_name='assets')
    op.drop_table('assets')
    op.drop_table('cubes')
    op.drop_index(op.f('ix_collection_items_composite_start'), table_name='collection_items')
    op.drop_index(op.f('ix_collection_items_composite_end'), table_name='collection_items')
    op.drop_table('collection_items')
    op.drop_table('band_compositions')
    op.drop_table('composite_functions')
    op.drop_table('collection_tiles')
    op.drop_table('bands')
    op.drop_table('asset_compositions')
    op.drop_index(op.f('ix_tiles_geom_wgs84'), table_name='tiles')
    op.drop_table('tiles')
    op.drop_table('collections')
    op.drop_table('temporal_composition_schemas')
    op.drop_table('spatial_resolution_schemas')
    op.drop_table('raster_chunk_schemas')
    op.drop_table('grs_schemas')
    # ### end Alembic commands ###
