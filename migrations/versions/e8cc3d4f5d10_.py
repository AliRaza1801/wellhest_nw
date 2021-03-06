"""empty message

Revision ID: e8cc3d4f5d10
Revises: 
Create Date: 2020-08-23 16:36:56.256617

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8cc3d4f5d10'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('user', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('user')
    )
    op.create_table('business_client',
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('business_name', sa.String(length=100), nullable=True),
    sa.Column('city', sa.String(length=50), nullable=True),
    sa.Column('address', sa.String(length=512), nullable=True),
    sa.Column('pin', sa.String(length=24), nullable=True),
    sa.Column('gstin', sa.String(length=64), nullable=True),
    sa.Column('pan', sa.String(length=64), nullable=True),
    sa.Column('mobile_number', sa.String(length=64), nullable=True),
    sa.Column('status', sa.String(length=10), nullable=True),
    sa.Column('category', sa.String(length=10), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user'], ),
    sa.PrimaryKeyConstraint('client_id')
    )
    op.create_table('features',
    sa.Column('feature_id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('wifi', sa.Boolean(), nullable=True),
    sa.Column('music', sa.Boolean(), nullable=True),
    sa.Column('ac', sa.Boolean(), nullable=True),
    sa.Column('disinfect', sa.Boolean(), nullable=True),
    sa.Column('parking', sa.Boolean(), nullable=True),
    sa.Column('organic', sa.Boolean(), nullable=True),
    sa.Column('safety', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['business_client.client_id'], ),
    sa.PrimaryKeyConstraint('feature_id')
    )
    op.create_table('products',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('loreal', sa.Boolean(), nullable=True),
    sa.Column('garnier', sa.Boolean(), nullable=True),
    sa.Column('streaks', sa.Boolean(), nullable=True),
    sa.Column('tresemme', sa.Boolean(), nullable=True),
    sa.Column('walla', sa.Boolean(), nullable=True),
    sa.Column('wahl', sa.Boolean(), nullable=True),
    sa.Column('mac', sa.Boolean(), nullable=True),
    sa.Column('mableme', sa.Boolean(), nullable=True),
    sa.Column('faces', sa.Boolean(), nullable=True),
    sa.Column('colorbar', sa.Boolean(), nullable=True),
    sa.Column('revlon', sa.Boolean(), nullable=True),
    sa.Column('shehnaaz', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['business_client.client_id'], ),
    sa.PrimaryKeyConstraint('product_id')
    )
    op.create_table('review',
    sa.Column('review_id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('ambience', sa.Boolean(), nullable=True),
    sa.Column('hygiene', sa.Boolean(), nullable=True),
    sa.Column('service', sa.Boolean(), nullable=True),
    sa.Column('staff', sa.Boolean(), nullable=True),
    sa.Column('facilities', sa.Boolean(), nullable=True),
    sa.Column('equipments', sa.Boolean(), nullable=True),
    sa.Column('trainer', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['business_client.client_id'], ),
    sa.PrimaryKeyConstraint('review_id')
    )
    op.create_table('services',
    sa.Column('service_id', sa.Integer(), nullable=False),
    sa.Column('gender', sa.String(length=64), nullable=True),
    sa.Column('category', sa.String(length=64), nullable=True),
    sa.Column('subcategory', sa.String(length=64), nullable=True),
    sa.Column('prices', sa.String(length=64), nullable=True),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['business_client.client_id'], ),
    sa.PrimaryKeyConstraint('service_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('services')
    op.drop_table('review')
    op.drop_table('products')
    op.drop_table('features')
    op.drop_table('business_client')
    op.drop_table('user')
    # ### end Alembic commands ###
