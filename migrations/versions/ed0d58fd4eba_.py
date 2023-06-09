"""empty message

Revision ID: ed0d58fd4eba
Revises: 4592a12cddfd
Create Date: 2023-04-14 10:48:47.912922

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed0d58fd4eba'
down_revision = '4592a12cddfd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.alter_column('customer',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.alter_column('customer',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
