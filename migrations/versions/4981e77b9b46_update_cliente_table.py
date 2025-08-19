"""UPDATE CLIENTE TABLE

Revision ID: 4981e77b9b46
Revises: f43ae25e29ff
Create Date: 2025-08-19 17:28:42.674560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4981e77b9b46'
down_revision = 'f43ae25e29ff'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('clientes', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
        batch_op.create_unique_constraint("uq_clientes_cpf_responsavel", ['cpf_responsavel'])


def downgrade():
    with op.batch_alter_table('clientes', schema=None) as batch_op:
        batch_op.drop_constraint("uq_clientes_cpf_responsavel", type_='unique')
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)


    # ### end Alembic commands ###
