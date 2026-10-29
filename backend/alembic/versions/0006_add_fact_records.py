"""Add evidence-linked manual fact records.

Revision ID: 0006_fact_records
Revises: 0005_scenarios
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0006_fact_records"
down_revision: Union[str, None] = "0005_scenarios"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "fact_records",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("case_id", sa.String(36), nullable=False),
        sa.Column("indicator_code", sa.String(16), nullable=False),
        sa.Column("raw_value_text", sa.String(5000), nullable=False),
        sa.Column("value_numeric", sa.String(64), nullable=True),
        sa.Column("value_text", sa.String(5000), nullable=True),
        sa.Column("unit", sa.String(64), nullable=True),
        sa.Column("currency", sa.String(8), nullable=True),
        sa.Column("period_start", sa.String(10), nullable=True),
        sa.Column("period_end", sa.String(10), nullable=True),
        sa.Column("as_of_date", sa.String(10), nullable=True),
        sa.Column("evidence_id", sa.String(36), nullable=False),
        sa.Column("entry_method", sa.String(24), nullable=False, server_default="manual"),
        sa.Column("review_status", sa.String(24), nullable=False, server_default="candidate"),
        sa.Column("definition_note", sa.String(2000), nullable=True),
        sa.Column("recorded_at", sa.String(40), nullable=False),
        sa.Column("created_at", sa.String(40), nullable=False),
        sa.Column("reviewed_at", sa.String(40), nullable=True),
        sa.Column("review_rationale", sa.String(2000), nullable=True),
        sa.Column("supersedes_fact_id", sa.String(36), nullable=True),
        sa.CheckConstraint("review_status IN ('candidate', 'accepted', 'rejected', 'conflicted', 'superseded')", name="ck_fact_records_review_status"),
        sa.CheckConstraint("entry_method IN ('manual', 'extracted_candidate', 'imported', 'connector', 'derived')", name="ck_fact_records_entry_method"),
        sa.ForeignKeyConstraint(["case_id"], ["research_cases.id"]),
        sa.ForeignKeyConstraint(["evidence_id"], ["evidence_items.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_fact_records_case_id", "fact_records", ["case_id"])
    op.create_index("ix_fact_records_indicator_code", "fact_records", ["indicator_code"])
    op.create_index("ix_fact_records_evidence_id", "fact_records", ["evidence_id"])
    op.create_index("ix_fact_records_review_status", "fact_records", ["review_status"])


def downgrade() -> None:
    op.drop_index("ix_fact_records_review_status", table_name="fact_records")
    op.drop_index("ix_fact_records_evidence_id", table_name="fact_records")
    op.drop_index("ix_fact_records_indicator_code", table_name="fact_records")
    op.drop_index("ix_fact_records_case_id", table_name="fact_records")
    op.drop_table("fact_records")
