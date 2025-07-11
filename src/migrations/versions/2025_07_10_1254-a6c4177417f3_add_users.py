"""add users

Revision ID: a6c4177417f3
Revises: 597e937e8f60
Create Date: 2025-07-10 12:54:50.362993

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a6c4177417f3"
down_revision: Union[str, None] = "597e937e8f60"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hash_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
