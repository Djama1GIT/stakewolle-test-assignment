"""some changes

Revision ID: 2a44f502ee29
Revises: cf0fc95b24da
Create Date: 2024-02-13 17:44:53.164660

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2a44f502ee29'
down_revision = 'cf0fc95b24da'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('referral_code_expiration', sa.DateTime(), nullable=True))
    op.drop_constraint('user_referral_code_key', 'user', type_='unique')
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_referral_code'), 'user', ['referral_code'], unique=True)
    op.drop_column('user', 'referral_expiration')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('referral_expiration', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_user_referral_code'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.create_unique_constraint('user_referral_code_key', 'user', ['referral_code'])
    op.drop_column('user', 'referral_code_expiration')
    # ### end Alembic commands ###
