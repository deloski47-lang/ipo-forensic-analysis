"""Add local evidence register.

Revision ID: 0002_evidence_items
Revises: 0001_research_cases
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002_evidence_items"
down_revision: Union[str, None] = "0001_research_cases"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "evidence_items",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("case_id", sa.String(36), nullable=False),
        sa.Column("evidence_kind", sa.String(32), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("source_url", sa.String(2048), nullable=True),
        sa.Column("original_file_name", sa.String(255), nullable=True),
        sa.Column("mime_type", sa.String(100), nullable=True),
        sa.Column("size_bytes", sa.Integer(), nullable=True),
        sa.Column("sha256", sa.String(64), nullable=True),
        sa.Column("published_at", sa.String(40), nullable=True),
        sa.Column("captured_at", sa.String(40), nullable=False),
        sa.Column("locator", sa.String(1000), nullable=True),
        sa.Column("verification_status", sa.String(24), nullable=False, server_default="unverified"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("local_relative_path", sa.String(500), nullable=True),
        sa.ForeignKeyConstraint(["case_id"], ["research_cases.id"], ondelete="CASCADE"),
        sa.CheckConstraint("evidence_kind IN ('web_page', 'manual_note', 'manual_value', 'document')", name="ck_evidence_items_kind"),
        sa.CheckConstraint("verification_status IN ('unverified', 'reviewed', 'conflicting', 'rejected')", name="ck_evidence_items_verification"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_evidence_items_case_id", "evidence_items", ["case_id"])
    op.create_index("ix_evidence_items_captured_at", "evidence_items", ["captured_at"])


def downgrade() -> None:
    op.drop_index("ix_evidence_items_captured_at", table_name="evidence_items")
    op.drop_index("ix_evidence_items_case_id", table_name="evidence_items")
    op.drop_table("evidence_items")
