"""create posts table

Revision ID: ec09e85e2ad6
Revises: 
Create Date: 2022-09-07 17:32:13.508288

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec09e85e2ad6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
