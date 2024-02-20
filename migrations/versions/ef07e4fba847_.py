"""empty message

Revision ID: ef07e4fba847
Revises: 1a36076538c3
Create Date: 2024-02-10 21:58:58.149482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef07e4fba847'
down_revision = '1a36076538c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product_item', schema=None) as batch_op:
        batch_op.alter_column('product_image',
               existing_type=sa.VARCHAR(length=300),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product_item', schema=None) as batch_op:
        batch_op.alter_column('product_image',
               existing_type=sa.VARCHAR(length=300),
               nullable=False)

    # ### end Alembic commands ###