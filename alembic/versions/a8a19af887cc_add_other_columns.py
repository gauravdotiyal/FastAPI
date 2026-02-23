"""add_other_columns

Revision ID: a8a19af887cc
Revises: f0b711d6bf0d
Create Date: 2026-02-23 01:24:54.922575

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8a19af887cc'
down_revision: Union[str, Sequence[str], None] = 'f0b711d6bf0d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
