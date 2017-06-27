"""add light_switch_state to sensor_data

Revision ID: e361748b3d99
Revises: 40efd4b5ddee
Create Date: 2017-06-27 20:41:23.199028

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e361748b3d99'
down_revision = '40efd4b5ddee'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'sensor_data',
        sa.Column('light_switch_state', sa.Boolean())
    )


def downgrade():
    op.drop_column('sensor_data', 'light_switch_state')
