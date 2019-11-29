"""初始化数据库

Revision ID: caf0448634a5
Revises: 
Create Date: 2019-11-29 10:28:58.758402

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'caf0448634a5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('t_channels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('remark', sa.Text(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('t_games',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('local_initshell_path', sa.String(length=200), nullable=True),
    sa.Column('remote_initshell_path', sa.String(length=200), nullable=True),
    sa.Column('local_open_service_pkg_path', sa.String(length=200), nullable=True),
    sa.Column('local_open_service_shell_path', sa.String(length=200), nullable=True),
    sa.Column('remote_open_service_pkg_path', sa.String(length=200), nullable=True),
    sa.Column('remote_open_service_shell_path', sa.String(length=200), nullable=True),
    sa.Column('local_update_pkg_path', sa.String(length=200), nullable=True),
    sa.Column('local_hot_update_shell_path', sa.String(length=200), nullable=True),
    sa.Column('local_cold_update_shell_path', sa.String(length=200), nullable=True),
    sa.Column('remote_update_pkg_path', sa.String(length=200), nullable=True),
    sa.Column('remote_hot_update_shell_path', sa.String(length=200), nullable=True),
    sa.Column('remote_cold_update_shell_path', sa.String(length=200), nullable=True),
    sa.Column('local_startservice_shell_path', sa.String(length=200), nullable=True),
    sa.Column('local_stopservice_shell_path', sa.String(length=200), nullable=True),
    sa.Column('remote_startservice_shell_path', sa.String(length=200), nullable=True),
    sa.Column('remote_stopservice_shell_path', sa.String(length=200), nullable=True),
    sa.Column('remote_unzip_path', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('t_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_t_user_email'), 't_user', ['email'], unique=True)
    op.create_index(op.f('ix_t_user_username'), 't_user', ['username'], unique=True)
    op.create_table('t_zones',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('zonenum', sa.String(length=30), nullable=True),
    sa.Column('zonename', sa.String(length=30), nullable=True),
    sa.Column('zoneip', sa.String(length=30), nullable=True),
    sa.Column('dblink', sa.String(length=30), nullable=True),
    sa.Column('dbport', sa.Integer(), nullable=True),
    sa.Column('db_A', sa.String(length=10), nullable=True),
    sa.Column('db_B', sa.String(length=10), nullable=True),
    sa.Column('db_C', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('membership',
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('channel_id', sa.Integer(), nullable=False),
    sa.Column('zone_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['channel_id'], ['t_channels.id'], ),
    sa.ForeignKeyConstraint(['game_id'], ['t_games.id'], ),
    sa.ForeignKeyConstraint(['zone_id'], ['t_zones.id'], ),
    sa.PrimaryKeyConstraint('game_id', 'channel_id', 'zone_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('membership')
    op.drop_table('t_zones')
    op.drop_index(op.f('ix_t_user_username'), table_name='t_user')
    op.drop_index(op.f('ix_t_user_email'), table_name='t_user')
    op.drop_table('t_user')
    op.drop_table('t_games')
    op.drop_table('t_channels')
    # ### end Alembic commands ###
