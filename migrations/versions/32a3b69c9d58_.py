"""empty message

Revision ID: 32a3b69c9d58
Revises: c97bd949105a
Create Date: 2020-09-23 23:10:33.519784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32a3b69c9d58'
down_revision = 'c97bd949105a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('business_client', sa.Column('description', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('business_client', 'description')
    # ### end Alembic commands ###
