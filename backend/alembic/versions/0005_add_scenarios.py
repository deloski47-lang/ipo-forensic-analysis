"""Add saved user-defined listing scenarios.

Revision ID: 0005_scenarios
Revises: 0004_market_observations
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0005_scenarios"
down_revision: Union[str, None] = "0004_market_observations"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "scenario_definitions",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("case_id", sa.String(36), nullable=False),
        sa.Column("label", sa.String(100), nullable=False),
        sa.Column("entry_price", sa.String(64), nullable=False),
        sa.Column("exit_price", sa.String(64), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=True),
        sa.Column("assumption_note", sa.String(2000), nullable=True),
        sa.Column("created_at", sa.String(40), nullable=False),
        sa.Column("updated_at", sa.String(40), nullable=False),
        sa.ForeignKeyConstraint(["case_id"], ["research_cases.id"]),
        sa.CheckConstraint("quantity IS NULL OR quantity >= 1", name="ck_scenario_definitions_quantity"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_scenario_definitions_case_id", "scenario_definitions", ["case_id"])


def downgrade() -> None:
    op.drop_index("ix_scenario_definitions_case_id", table_name="scenario_definitions")
    op.drop_table("scenario_definitions")
