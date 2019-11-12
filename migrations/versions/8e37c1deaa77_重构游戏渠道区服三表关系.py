"""重构游戏渠道区服三表关系

Revision ID: 8e37c1deaa77
Revises: 678b02f1d7a1
Create Date: 2019-11-12 12:44:46.195197

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8e37c1deaa77'
down_revision = '678b02f1d7a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('membership', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('membership', sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False))
    # ### end Alembic commands ###
