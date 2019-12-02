"""zone表增加状态字段v1

Revision ID: 69e65dfc01be
Revises: d7a1debd80d3
Create Date: 2019-12-02 03:34:21.882576

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69e65dfc01be'
down_revision = 'd7a1debd80d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('t_zones', sa.Column('status', sa.Boolean(), server_default=sa.text('true'), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('t_zones', 'status')
    # ### end Alembic commands ###
