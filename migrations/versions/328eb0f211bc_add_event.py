"""add event

Revision ID: 328eb0f211bc
Revises: 59628dea39ff
Create Date: 2024-04-14 09:56:14.289980

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision = '328eb0f211bc'
down_revision = '59628dea39ff'
branch_labels = None
depends_on = None


def upgrade():
    StatusEnum = sa.Enum('TODO', 'IN_PROGRESS', 'COMPLETED', name='StatusEnum')
    op.create_table('event',
                    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
                    sa.Column('title', sa.String(length=255), nullable=False),
                    sa.Column('description', sa.String(length=255), nullable=True),
                    sa.Column('status', sa.String(length=255), nullable=False),
                    sa.Column('startTime', sa.DateTime(), nullable=True),
                    sa.Column('endTime', sa.DateTime(), nullable=True),
                    sa.Column("created_at", sa.DateTime(), nullable=False),
                    sa.Column("updated_at", sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.execute("ALTER TABLE event MODIFY COLUMN status ENUM('TODO', 'IN_PROGRESS', 'COMPLETED') NOT NULL")
    op.create_table('event_user',
                    sa.Column('event_id', sa.BigInteger(), nullable=False),
                    sa.Column('user_id', sa.BigInteger(), nullable=False),
                    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
                    )


def downgrade():
    op.drop_table('event_user')
    op.drop_table('event')

