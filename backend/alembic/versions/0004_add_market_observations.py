"""Add manual market observation history.

Revision ID: 0004_market_observations
Revises: 0003_identity
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0004_market_observations"
down_revision: Union[str, None] = "0003_identity"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "market_observations",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("case_id", sa.String(36), nullable=False),
        sa.Column("indicator_code", sa.String(16), nullable=False),
        sa.Column("signal_category", sa.String(32), nullable=False),
        sa.Column("segment", sa.String(16), nullable=True),
        sa.Column("raw_value_text", sa.String(5000), nullable=False),
        sa.Column("value_numeric", sa.String(64), nullable=True),
        sa.Column("value_text", sa.String(5000), nullable=True),
        sa.Column("unit", sa.String(64), nullable=True),
        sa.Column("currency", sa.String(8), nullable=True),
        sa.Column("metric_definition", sa.String(2000), nullable=False),
        sa.Column("observed_at", sa.String(40), nullable=True),
        sa.Column("published_at", sa.String(40), nullable=True),
        sa.Column("retrieved_at", sa.String(40), nullable=True),
        sa.Column("recorded_at", sa.String(40), nullable=False),
        sa.Column("source_id", sa.String(36), nullable=True),
        sa.Column("acquisition_attempt_id", sa.String(36), nullable=True),
        sa.Column("evidence_id", sa.String(36), nullable=False),
        sa.Column("entry_method", sa.String(24), nullable=False, server_default="manual"),
        sa.Column("review_status", sa.String(24), nullable=False, server_default="candidate"),
        sa.Column("definition_metadata_json", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("reviewed_at", sa.String(40), nullable=True),
        sa.Column("review_rationale", sa.String(2000), nullable=True),
        sa.Column("supersedes_observation_id", sa.String(36), nullable=True),
        sa.CheckConstraint("signal_category IN ('issue_terms', 'company_financials', 'valuation', 'subscription_qib', 'subscription_nii', 'subscription_retail', 'gmp', 'market_context', 'company_events')", name="ck_market_observations_signal_category"),
        sa.CheckConstraint("review_status IN ('candidate', 'accepted', 'rejected', 'conflicted', 'superseded')", name="ck_market_observations_review_status"),
        sa.CheckConstraint("entry_method IN ('manual', 'extracted_candidate', 'imported', 'connector', 'derived')", name="ck_market_observations_entry_method"),
        sa.ForeignKeyConstraint(["case_id"], ["research_cases.id"]),
        sa.ForeignKeyConstraint(["evidence_id"], ["evidence_items.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_market_observations_case_id", "market_observations", ["case_id"])
    op.create_index("ix_market_observations_indicator_code", "market_observations", ["indicator_code"])
    op.create_index("ix_market_observations_signal_category", "market_observations", ["signal_category"])
    op.create_index("ix_market_observations_review_status", "market_observations", ["review_status"])
    op.create_index("ix_market_observations_evidence_id", "market_observations", ["evidence_id"])


def downgrade() -> None:
    op.drop_index("ix_market_observations_evidence_id", table_name="market_observations")
    op.drop_index("ix_market_observations_review_status", table_name="market_observations")
    op.drop_index("ix_market_observations_signal_category", table_name="market_observations")
    op.drop_index("ix_market_observations_indicator_code", table_name="market_observations")
    op.drop_index("ix_market_observations_case_id", table_name="market_observations")
    op.drop_table("market_observations")
