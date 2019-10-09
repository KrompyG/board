"""product table

Revision ID: 0f46f1084b64
Revises: 5fbed0e1ee33
Create Date: 2019-09-14 15:51:09.032242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f46f1084b64'
down_revision = '5fbed0e1ee33'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
	
	#category table
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_category_name'), 'category', ['name'], unique=False)

	#product table
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
	sa.Column('photo_name', sa.String(length=256), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id']),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id']),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_timestamp'), 'product', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_product_timestamp'), table_name='product')
    op.drop_table('product')
    op.drop_index(op.f('ix_category_name'), table_name='category')
    op.drop_table('category')
    # ### end Alembic commands ###
