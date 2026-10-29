"""Add immutable report snapshots and local export artifacts.

Revision ID: 0008_reports
Revises: 0007_analysis_runs
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0008_reports"
down_revision: Union[str, None] = "0007_analysis_runs"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "reports",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("case_id", sa.String(36), nullable=False),
        sa.Column("analysis_run_id", sa.String(36), nullable=False),
        sa.Column("generated_at", sa.String(40), nullable=False),
        sa.Column("template_version", sa.String(32), nullable=False),
        sa.Column("report_snapshot_hash", sa.String(64), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("issue_display_name", sa.String(200), nullable=False),
        sa.Column("information_cutoff_at", sa.String(40), nullable=False),
        sa.Column("snapshot_json", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["case_id"], ["research_cases.id"]),
        sa.ForeignKeyConstraint(["analysis_run_id"], ["analysis_runs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_reports_case_id", "reports", ["case_id"])
    op.create_index("ix_reports_analysis_run_id", "reports", ["analysis_run_id"])
    op.create_table(
        "report_artifacts",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("report_id", sa.String(36), nullable=False),
        sa.Column("format", sa.String(8), nullable=False),
        sa.Column("sha256", sa.String(64), nullable=False),
        sa.Column("size_bytes", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.String(40), nullable=False),
        sa.Column("local_relative_path", sa.String(500), nullable=False),
        sa.CheckConstraint("format IN ('html', 'docx')", name="ck_report_artifacts_format"),
        sa.ForeignKeyConstraint(["report_id"], ["reports.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_report_artifacts_report_id", "report_artifacts", ["report_id"])


def downgrade() -> None:
    op.drop_index("ix_report_artifacts_report_id", table_name="report_artifacts")
    op.drop_table("report_artifacts")
    op.drop_index("ix_reports_analysis_run_id", table_name="reports")
    op.drop_index("ix_reports_case_id", table_name="reports")
    op.drop_table("reports")
