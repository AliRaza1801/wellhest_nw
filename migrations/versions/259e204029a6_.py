"""empty message

Revision ID: 259e204029a6
Revises: 9b1595a4c40d
Create Date: 2020-10-10 19:11:23.338077

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '259e204029a6'
down_revision = '9b1595a4c40d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart', sa.Column('booking_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cart', 'booking_at')
    # ### end Alembic commands ###
