"""Add validated restore archive records.

Revision ID: 0009_restore_validations
Revises: 0008_reports
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0009_restore_validations"
down_revision: Union[str, None] = "0008_reports"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "restore_validations",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("archive_relative_path", sa.String(500), nullable=False),
        sa.Column("archive_sha256", sa.String(64), nullable=False),
        sa.Column("archive_size_bytes", sa.Integer(), nullable=False),
        sa.Column("case_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("evidence_file_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("warnings_json", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("errors_json", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("validated_at", sa.String(40), nullable=False),
        sa.CheckConstraint("status IN ('valid', 'invalid', 'incompatible')", name="ck_restore_validations_status"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("restore_validations")
