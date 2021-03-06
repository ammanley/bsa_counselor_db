"""empty message

Revision ID: 565b551e39a5
Revises: 56c64bb7c148
Create Date: 2017-02-24 09:35:18.939278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '565b551e39a5'
down_revision = '56c64bb7c148'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('merit_badges',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('eagle_required', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('merit_badges')
    # ### end Alembic commands ###
