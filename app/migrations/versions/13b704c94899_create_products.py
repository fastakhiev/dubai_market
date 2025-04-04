"""create products

Revision ID: 13b704c94899
Revises: 08087963c415
Create Date: 2025-03-27 17:51:12.793609

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY, UUID


# revision identifiers, used by Alembic.
revision: str = '13b704c94899'
down_revision: Union[str, None] = '08087963c415'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'products',
        sa.Column('id', UUID(as_uuid=True)),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('price', sa.Numeric(10, 2), nullable=False),
        sa.Column('currency', sa.String(10), nullable=False, default='USD'),
        sa.Column('seller_id', UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, default='active'),
        sa.Column('photos', sa.JSON(), nullable=True),
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id")
    )

def downgrade():
    op.drop_table('products')
