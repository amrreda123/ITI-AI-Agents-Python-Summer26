"""add ai summary column

Revision ID: 002_add_ai_summary
Revises: 001_initial_documents_schema
Create Date: 2026-09-14 13:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "002_add_ai_summary"
down_revision: Union[str, None] = "001_initial_documents_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("documents", schema=None) as batch_op:
        batch_op.add_column(sa.Column("ai_summary", sa.Text(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table("documents", schema=None) as batch_op:
        batch_op.drop_column("ai_summary")
