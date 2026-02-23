"""Adding users table

Revision ID: ad8bad6972d6
Revises: 3abbfe9a5499
Create Date: 2026-02-23 01:02:01.507488

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad8bad6972d6'
down_revision: Union[str, Sequence[str], None] = '3abbfe9a5499'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_tabel('users')
    pass
