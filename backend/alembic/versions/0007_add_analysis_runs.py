"""Add immutable analysis run snapshots, results and findings.

Revision ID: 0007_analysis_runs
Revises: 0006_fact_records
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0007_analysis_runs"
down_revision: Union[str, None] = "0006_fact_records"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "analysis_runs",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("case_id", sa.String(36), nullable=False),
        sa.Column("run_status", sa.String(16), nullable=False),
        sa.Column("information_cutoff_at", sa.String(40), nullable=False),
        sa.Column("started_at", sa.String(40), nullable=False),
        sa.Column("finished_at", sa.String(40), nullable=True),
        sa.Column("schema_version", sa.String(24), nullable=False),
        sa.Column("formula_set_version", sa.String(64), nullable=False),
        sa.Column("rule_set_version", sa.String(64), nullable=False),
        sa.Column("software_version", sa.String(24), nullable=False),
        sa.Column("input_snapshot_hash", sa.String(64), nullable=False),
        sa.Column("input_snapshot_json", sa.Text(), nullable=False),
        sa.Column("readiness_json", sa.Text(), nullable=False),
        sa.Column("error_summary", sa.String(2000), nullable=True),
        sa.CheckConstraint("run_status IN ('completed', 'partial', 'failed')", name="ck_analysis_runs_status"),
        sa.ForeignKeyConstraint(["case_id"], ["research_cases.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_analysis_runs_case_id", "analysis_runs", ["case_id"])
    op.create_table(
        "analysis_results",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("analysis_run_id", sa.String(36), nullable=False),
        sa.Column("indicator_code", sa.String(16), nullable=False),
        sa.Column("calculation_status", sa.String(24), nullable=False),
        sa.Column("value_decimal", sa.String(64), nullable=True),
        sa.Column("value_text", sa.String(5000), nullable=True),
        sa.Column("unit", sa.String(64), nullable=True),
        sa.Column("currency", sa.String(8), nullable=True),
        sa.Column("display_value", sa.String(128), nullable=True),
        sa.Column("formula_code", sa.String(64), nullable=True),
        sa.Column("formula_version", sa.String(64), nullable=True),
        sa.Column("input_fact_ids_json", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("input_observation_ids_json", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("evidence_ids_json", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("explanation", sa.String(5000), nullable=False),
        sa.Column("reason", sa.String(2000), nullable=True),
        sa.ForeignKeyConstraint(["analysis_run_id"], ["analysis_runs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_analysis_results_analysis_run_id", "analysis_results", ["analysis_run_id"])
    op.create_table(
        "findings",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("analysis_run_id", sa.String(36), nullable=False),
        sa.Column("rule_code", sa.String(64), nullable=False),
        sa.Column("rule_version", sa.String(64), nullable=False),
        sa.Column("finding_type", sa.String(32), nullable=False),
        sa.Column("severity", sa.String(16), nullable=False),
        sa.Column("status", sa.String(16), nullable=False, server_default="active"),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("explanation", sa.String(5000), nullable=False),
        sa.Column("limitation_note", sa.String(2000), nullable=True),
        sa.Column("related_indicator_codes_json", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("input_fact_ids_json", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("input_observation_ids_json", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("evidence_links_json", sa.Text(), nullable=False, server_default="[]"),
        sa.ForeignKeyConstraint(["analysis_run_id"], ["analysis_runs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_findings_analysis_run_id", "findings", ["analysis_run_id"])


def downgrade() -> None:
    op.drop_index("ix_findings_analysis_run_id", table_name="findings")
    op.drop_table("findings")
    op.drop_index("ix_analysis_results_analysis_run_id", table_name="analysis_results")
    op.drop_table("analysis_results")
    op.drop_index("ix_analysis_runs_case_id", table_name="analysis_runs")
    op.drop_table("analysis_runs")
