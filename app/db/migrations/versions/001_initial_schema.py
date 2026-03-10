"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2026-01-08 15:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create scenes table
    op.create_table(
        'scenes',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('initial_state', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('exit_conditions', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_scenes_name'), 'scenes', ['name'], unique=True)
    
    # Create characters table
    op.create_table(
        'characters',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('personality', sa.Text(), nullable=False),
        sa.Column('background', sa.Text(), nullable=False),
        sa.Column('scene_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['scene_id'], ['scenes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_characters_name'), 'characters', ['name'], unique=False)
    op.create_index(op.f('ix_characters_scene_id'), 'characters', ['scene_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_characters_scene_id'), table_name='characters')
    op.drop_index(op.f('ix_characters_name'), table_name='characters')
    op.drop_table('characters')
    op.drop_index(op.f('ix_scenes_name'), table_name='scenes')
    op.drop_table('scenes')
