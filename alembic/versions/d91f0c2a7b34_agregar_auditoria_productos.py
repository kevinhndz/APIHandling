"""Add audit columns to Productos

Revision ID: d91f0c2a7b34
Revises: afe62bc9678c
Create Date: 2026-10-01
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "d91f0c2a7b34"
down_revision: Union[str, Sequence[str], None] = "afe62bc9678c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "Productos",
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )
    op.add_column(
        "Productos",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )


def downgrade() -> None:
    op.drop_column("Productos", "updated_at")
    op.drop_column("Productos", "created_at")
