"""auto Added account table

Revision ID: 40b9dc930bf6
Revises: d8fb4c09770e
Create Date: 2022-07-24 22:09:42.146568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40b9dc930bf6'
down_revision = 'd8fb4c09770e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('friends', sa.Column('created_on', sa.DateTime(), nullable=True))
    op.create_unique_constraint(None, 'users', ['user_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('friends', 'created_on')
    # ### end Alembic commands ###
