"""template_items

Revision ID: ffb46bba46c4
Revises: a6b25d7471c8
Create Date: 2020-07-09 11:17:47.694445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffb46bba46c4'
down_revision = '4f11161cb5a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('template_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('platform', sa.String(length=64), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('logo', sa.Text(), nullable=True),
    sa.Column('image', sa.String(length=128), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('categories', sa.JSON(), nullable=True),
    sa.Column('restart_policy', sa.String(length=20), nullable=True),
    sa.Column('ports', sa.JSON(), nullable=True),
    sa.Column('volumes', sa.JSON(), nullable=True),
    sa.Column('env', sa.JSON(), nullable=True),
    sa.Column('sysctls', sa.JSON(), nullable=True),
    sa.Column('cap_add', sa.JSON(), nullable=True),
    sa.Column('template_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['template_id'], ['templates.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_template_item_name'), 'template_item', ['name'], unique=False)
    op.create_index(op.f('ix_template_item_title'), 'template_item', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_template_item_title'), table_name='template_item')
    op.drop_index(op.f('ix_template_item_name'), table_name='template_item')
    op.drop_table('template_item')
    # ### end Alembic commands ###
