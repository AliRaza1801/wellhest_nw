"""empty message

Revision ID: a760ab285ac1
Revises: 8a41b71144f7
Create Date: 2020-10-22 18:36:25.325855

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a760ab285ac1'
down_revision = '8a41b71144f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payment',
    sa.Column('booking_id', sa.Integer(), nullable=False),
    sa.Column('payment_id', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('booking_id')
    )
    op.create_table('user',
    sa.Column('user', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('mobile_number', sa.String(length=64), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('user')
    )
    op.create_table('business_client',
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('business_name', sa.String(length=100), nullable=True),
    sa.Column('city', sa.String(length=50), nullable=True),
    sa.Column('locality', sa.String(length=255), nullable=True),
    sa.Column('address', sa.String(length=512), nullable=True),
    sa.Column('pin', sa.String(length=24), nullable=True),
    sa.Column('lat', sa.String(length=24), nullable=True),
    sa.Column('lng', sa.String(length=24), nullable=True),
    sa.Column('place_id', sa.String(length=64), nullable=True),
    sa.Column('gstin', sa.String(length=64), nullable=True),
    sa.Column('pan', sa.String(length=64), nullable=True),
    sa.Column('mobile_number', sa.String(length=64), nullable=True),
    sa.Column('manager_name', sa.String(length=255), nullable=True),
    sa.Column('mobile_number_manager', sa.String(length=64), nullable=True),
    sa.Column('status', sa.String(length=10), nullable=True),
    sa.Column('category', sa.String(length=10), nullable=True),
    sa.Column('license_number', sa.String(length=255), nullable=True),
    sa.Column('business_id', sa.String(length=255), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('partnership', sa.String(length=20), nullable=True),
    sa.Column('business_type', sa.String(length=20), nullable=True),
    sa.Column('updated', sa.Boolean(), nullable=True),
    sa.Column('open_time', sa.Time(), nullable=True),
    sa.Column('close_time', sa.Time(), nullable=True),
    sa.Column('day_from', sa.String(length=20), nullable=True),
    sa.Column('day_to', sa.String(length=20), nullable=True),
    sa.Column('otp', sa.String(length=20), nullable=True),
    sa.Column('otp_verified', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user'], ),
    sa.PrimaryKeyConstraint('client_id')
    )
    op.create_table('ambience_image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('image', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['business_client.client_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('booking',
    sa.Column('booking_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('payment_id', sa.Integer(), nullable=True),
    sa.Column('customer_name', sa.String(length=255), nullable=True),
    sa.Column('customer_email', sa.String(length=255), nullable=True),
    sa.Column('mobile_number', sa.String(length=255), nullable=True),
    sa.Column('business_id', sa.Integer(), nullable=True),
    sa.Column('payment_mode', sa.String(length=255), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('amount', sa.String(length=255), nullable=True),
    sa.Column('paid', sa.Boolean(), nullable=True),
    sa.Column('booking_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['business_id'], ['business_client.client_id'], ),
    sa.ForeignKeyConstraint(['payment_id'], ['payment.booking_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user'], ),
    sa.PrimaryKeyConstraint('booking_id')
    )
    op.create_table('centre_image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('image', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['business_client.client_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('equipments_image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('image', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['business_client.client_id'], ),
    sa.PrimaryKeyConstraint('id')
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
    op.create_table('service_image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('image', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['business_client.client_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('services',
    sa.Column('service_id', sa.Integer(), nullable=False),
    sa.Column('gender', sa.String(length=64), nullable=True),
    sa.Column('category', sa.String(length=64), nullable=True),
    sa.Column('subcategory', sa.String(length=64), nullable=True),
    sa.Column('service', sa.String(length=64), nullable=True),
    sa.Column('prices', sa.String(length=64), nullable=True),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['business_client.client_id'], ),
    sa.PrimaryKeyConstraint('service_id')
    )
    op.create_table('staff_image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('image', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['business_client.client_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('booking_services',
    sa.Column('booking_services_id', sa.Integer(), nullable=False),
    sa.Column('service_id', sa.Integer(), nullable=True),
    sa.Column('booking_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['booking_id'], ['booking.booking_id'], ),
    sa.ForeignKeyConstraint(['service_id'], ['services.service_id'], ),
    sa.PrimaryKeyConstraint('booking_services_id')
    )
    op.create_table('cart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('service_id', sa.Integer(), nullable=True),
    sa.Column('business_id', sa.Integer(), nullable=True),
    sa.Column('booking_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['business_id'], ['business_client.client_id'], ),
    sa.ForeignKeyConstraint(['service_id'], ['services.service_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cart')
    op.drop_table('booking_services')
    op.drop_table('staff_image')
    op.drop_table('services')
    op.drop_table('service_image')
    op.drop_table('review')
    op.drop_table('products')
    op.drop_table('features')
    op.drop_table('equipments_image')
    op.drop_table('centre_image')
    op.drop_table('booking')
    op.drop_table('ambience_image')
    op.drop_table('business_client')
    op.drop_table('user')
    op.drop_table('payment')
    # ### end Alembic commands ###
