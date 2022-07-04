"""added new column

Revision ID: eebb82078eec
Revises: 
Create Date: 2022-06-20 23:27:39.318192

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eebb82078eec'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'visitations', 'abc_families', ['family_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'visitations', type_='foreignkey')
    # ### end Alembic commands ###
