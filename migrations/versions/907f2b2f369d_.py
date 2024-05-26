"""empty message

Revision ID: 907f2b2f369d
Revises: 
Create Date: 2024-05-25 11:29:41.940608

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '907f2b2f369d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('membership',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('duration_days', sa.Integer(), nullable=True),
    sa.Column('classes_per_month', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('movement_images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('img_data', sa.LargeBinary(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('profile_image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('img_data', sa.LargeBinary(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role_permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('permission_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['permission_id'], ['permission.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=250), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('last_name', sa.String(length=80), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('registration_date', sa.DateTime(), nullable=True),
    sa.Column('last_update_date', sa.DateTime(), nullable=True),
    sa.Column('image_url', sa.String(length=255), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('profile_image_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['profile_image_id'], ['profile_image.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('payment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('membership_id', sa.Integer(), nullable=False),
    sa.Column('payment_date', sa.DateTime(), nullable=True),
    sa.Column('confirmation_date', sa.DateTime(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('payment_method', sa.String(length=50), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('transaction_reference', sa.String(length=255), nullable=True),
    sa.Column('currency', sa.String(length=3), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('card_number_last4', sa.String(length=4), nullable=True),
    sa.Column('card_type', sa.String(length=255), nullable=True),
    sa.Column('cardholder_name', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['membership_id'], ['membership.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('security_question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question', sa.String(length=255), nullable=False),
    sa.Column('answer', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('training_classes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('dateTime_class', sa.DateTime(), nullable=True),
    sa.Column('Class_is_active', sa.Boolean(), nullable=True),
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.Column('duration_minutes', sa.Integer(), nullable=False),
    sa.Column('available_slots', sa.Integer(), nullable=False),
    sa.Column('instructor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['instructor_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_membership_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('membership_id', sa.Integer(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('remaining_classes', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['membership_id'], ['membership.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('booking',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('training_class_id', sa.Integer(), nullable=False),
    sa.Column('booking_date', sa.DateTime(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['training_class_id'], ['training_classes.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payment_detail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('payment_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('product_description', sa.String(length=255), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('unit_price', sa.Float(), nullable=False),
    sa.Column('subtotal', sa.Float(), nullable=False),
    sa.Column('tax_amount', sa.Float(), nullable=False),
    sa.Column('discount_amount', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['payment_id'], ['payment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payment_detail')
    op.drop_table('booking')
    op.drop_table('user_membership_history')
    op.drop_table('training_classes')
    op.drop_table('security_question')
    op.drop_table('payment')
    op.drop_table('user')
    op.drop_table('role_permission')
    op.drop_table('role')
    op.drop_table('profile_image')
    op.drop_table('permission')
    op.drop_table('movement_images')
    op.drop_table('membership')
    # ### end Alembic commands ###
