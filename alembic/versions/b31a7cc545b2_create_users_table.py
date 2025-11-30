"""create users table

Revision ID: b31a7cc545b2
Revises: 
Create Date: 2025-11-22 19:34:29.397996

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b31a7cc545b2'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.UUID, primary_key=True),
        sa.Column("name", sa.String),
        sa.Column("email", sa.String, unique=True),
        sa.Column("password", sa.String),
        sa.Column("active", sa.Boolean, server_default=sa.text('true')),
        sa.Column("last_login_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
