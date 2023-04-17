"""empty message

Revision ID: 97d818974ce9
Revises: 6b81da6ec533
Create Date: 2023-04-16 07:45:57.441737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97d818974ce9'
down_revision = '6b81da6ec533'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.alter_column('customer',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.alter_column('customer',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
