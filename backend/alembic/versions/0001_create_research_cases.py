"""Create initial research cases table.

Revision ID: 0001_research_cases
Revises:
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001_research_cases"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "research_cases",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("entered_name", sa.String(length=200), nullable=False),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("case_status", sa.String(length=32), nullable=False, server_default="identity_pending"),
        sa.Column("identity_status", sa.String(length=32), nullable=False, server_default="unresolved"),
        sa.Column("issue_id", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.String(length=40), nullable=False),
        sa.Column("updated_at", sa.String(length=40), nullable=False),
        sa.Column("last_activity_at", sa.String(length=40), nullable=False),
        sa.Column("latest_analysis_run_id", sa.String(length=36), nullable=True),
        sa.Column("latest_report_id", sa.String(length=36), nullable=True),
        sa.Column("case_changed_since_last_run", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("readiness_summary", sa.String(length=16), nullable=True),
        sa.Column("warning_count", sa.Integer(), nullable=False, server_default="0"),
        sa.CheckConstraint("case_status IN ('identity_pending', 'active', 'archived')", name="ck_research_cases_status"),
        sa.CheckConstraint(
            "identity_status IN ('unresolved', 'ambiguous', 'confirmed', 'out_of_scope', 'rejected')",
            name="ck_research_cases_identity_status",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_research_cases_case_status", "research_cases", ["case_status"])
    op.create_index("ix_research_cases_last_activity_at", "research_cases", ["last_activity_at"])


def downgrade() -> None:
    op.drop_index("ix_research_cases_last_activity_at", table_name="research_cases")
    op.drop_index("ix_research_cases_case_status", table_name="research_cases")
    op.drop_table("research_cases")
