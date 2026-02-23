"""add content column

Revision ID: 3abbfe9a5499
Revises: 99105968ed43
Create Date: 2026-02-23 00:46:34.395912

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3abbfe9a5499'
down_revision: Union[str, Sequence[str], None] = '99105968ed43'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False ) )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
