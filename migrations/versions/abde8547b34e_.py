"""empty message

Revision ID: abde8547b34e
Revises: ef07e4fba847
Create Date: 2024-02-10 23:38:24.260280

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abde8547b34e'
down_revision = 'ef07e4fba847'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product_item', schema=None) as batch_op:
        batch_op.drop_constraint('product_item_size_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('product_item_product_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('product_item_material_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('product_item_crystal_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'crystal', ['crystal_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'size', ['size_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'products', ['product_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'material', ['material_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product_item', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('product_item_crystal_id_fkey', 'crystal', ['crystal_id'], ['id'])
        batch_op.create_foreign_key('product_item_material_id_fkey', 'material', ['material_id'], ['id'])
        batch_op.create_foreign_key('product_item_product_id_fkey', 'products', ['product_id'], ['id'])
        batch_op.create_foreign_key('product_item_size_id_fkey', 'size', ['size_id'], ['id'])

    # ### end Alembic commands ###