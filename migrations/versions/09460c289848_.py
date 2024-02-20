"""empty message

Revision ID: 09460c289848
Revises: abde8547b34e
Create Date: 2024-02-17 15:57:14.277896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09460c289848'
down_revision = 'abde8547b34e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('promotion', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'product_category', ['category_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('promotion', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('category_id')

    # ### end Alembic commands ###