"""create sensor_data table

Revision ID: 40efd4b5ddee
Revises: 
Create Date: 2017-06-25 17:25:44.000458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40efd4b5ddee'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'sensor_data',
        sa.Column(
            'recorded_at',
            sa.DateTime,
            server_default=sa.func.current_timestamp(),
            primary_key=True
        ),
        sa.Column('light_infrared', sa.Integer),
        sa.Column('light_visible', sa.Integer),
        sa.Column('light_lux', sa.Float(precision=4)),
        sa.Column('pressure', sa.Float(precision=4)),
        sa.Column('temperature', sa.Float(precision=4)),
        sa.Column('humidity', sa.Float(precision=4)),
        sa.Column('soil_moisture', sa.Float(precision=4))
    )


def downgrade():
    op.drop_table('sensor_data')
