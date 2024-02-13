"""ref

Revision ID: f7b23a37c516
Revises: bbbd55ca18b8
Create Date: 2024-02-13 06:54:54.387550

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7b23a37c516'
down_revision = 'bbbd55ca18b8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('referrer_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'user', ['referrer_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'referrer_id')
    # ### end Alembic commands ###
