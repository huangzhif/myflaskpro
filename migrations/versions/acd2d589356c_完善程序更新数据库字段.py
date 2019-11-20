"""完善程序更新数据库字段

Revision ID: acd2d589356c
Revises: de91c3c508a7
Create Date: 2019-11-20 11:34:38.273434

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'acd2d589356c'
down_revision = 'de91c3c508a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('t_channels', 'remark',
               existing_type=mysql.TEXT(),
               type_=sa.Text(length=500),
               existing_nullable=True)
    op.add_column('t_games', sa.Column('local_update_pkg_path', sa.String(length=200), nullable=True))
    op.add_column('t_games', sa.Column('local_update_shell_path', sa.String(length=200), nullable=True))
    op.add_column('t_games', sa.Column('remote_update_pkg_path', sa.String(length=200), nullable=True))
    op.add_column('t_games', sa.Column('remote_update_shell_path', sa.String(length=200), nullable=True))
    op.alter_column('t_user', 'is_active',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('t_user', 'is_active',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.drop_column('t_games', 'remote_update_shell_path')
    op.drop_column('t_games', 'remote_update_pkg_path')
    op.drop_column('t_games', 'local_update_shell_path')
    op.drop_column('t_games', 'local_update_pkg_path')
    op.alter_column('t_channels', 'remark',
               existing_type=sa.Text(length=500),
               type_=mysql.TEXT(),
               existing_nullable=True)
    # ### end Alembic commands ###
