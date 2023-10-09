"""empty message

Revision ID: 37d5562749ec
Revises: 68911bd5e674
Create Date: 2023-09-14 02:04:30.728579

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37d5562749ec'
down_revision = '68911bd5e674'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('description', sa.String(length=1000), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(precision=4, asdecimal=2), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('association_table_orders',
    sa.Column('products', sa.Integer(), nullable=True),
    sa.Column('ordenes', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ordenes'], ['ordenes.id'], ),
    sa.ForeignKeyConstraint(['products'], ['products.id'], )
    )
    with op.batch_alter_table('ordenes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('delivery_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('custumer_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'driver', ['delivery_id'], ['id'])
        batch_op.create_foreign_key(None, 'customer', ['custumer_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ordenes', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('custumer_id')
        batch_op.drop_column('delivery_id')

    op.drop_table('association_table_orders')
    op.drop_table('products')
    # ### end Alembic commands ###
