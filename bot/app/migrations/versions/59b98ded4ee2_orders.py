"""orders

Revision ID: 59b98ded4ee2
Revises: 13b704c94899
Create Date: 2025-04-24 07:18:27.459875

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import nullsfirst
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '59b98ded4ee2'
down_revision: Union[str, None] = '13b704c94899'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "orders",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "product_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("products.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "buyer_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=False
        ),
        sa.Column("destination", sa.String(), nullable=False),
        sa.Column("seller_comment", sa.String(), nullable=True),
        sa.Column("buyer_comment", sa.String(), nullable=True),
        sa.Column("is_approve", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id")
    )


def downgrade() -> None:
    op.drop_table("orders")
