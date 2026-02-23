"""add foreign key to the post table 

Revision ID: f0b711d6bf0d
Revises: ad8bad6972d6
Create Date: 2026-02-23 01:14:14.917596

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0b711d6bf0d'
down_revision: Union[str, Sequence[str], None] = 'ad8bad6972d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False) )
    op.create_foreign_key('posts_user_fk', source_table='posts', referent_table='users', local_cols=['owner_id'] , remote_cols=['id'], ondelete="CASCADE"   )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('posts_user_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
