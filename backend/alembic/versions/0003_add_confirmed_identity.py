"""Add issuer and confirmed Mainboard IPO issue tables.

Revision ID: 0003_identity
Revises: 0002_evidence_items
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0003_identity"
down_revision: Union[str, None] = "0002_evidence_items"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "issuers",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("legal_name", sa.String(200), nullable=False),
        sa.Column("created_at", sa.String(40), nullable=False),
        sa.Column("updated_at", sa.String(40), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "ipo_issues",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("issuer_id", sa.String(36), nullable=False),
        sa.Column("display_name", sa.String(200), nullable=False),
        sa.Column("market_segment", sa.String(16), nullable=False, server_default="MAINBOARD"),
        sa.Column("open_date", sa.String(10), nullable=True),
        sa.Column("close_date", sa.String(10), nullable=True),
        sa.Column("listing_date", sa.String(10), nullable=True),
        sa.Column("price_band_low", sa.String(64), nullable=True),
        sa.Column("price_band_high", sa.String(64), nullable=True),
        sa.Column("issue_size_amount", sa.String(64), nullable=True),
        sa.Column("issue_size_unit", sa.String(32), nullable=True),
        sa.Column("created_at", sa.String(40), nullable=False),
        sa.Column("updated_at", sa.String(40), nullable=False),
        sa.CheckConstraint("market_segment = 'MAINBOARD'", name="ck_ipo_issues_mainboard_only"),
        sa.ForeignKeyConstraint(["issuer_id"], ["issuers.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ipo_issues_issuer_id", "ipo_issues", ["issuer_id"])


def downgrade() -> None:
    op.drop_index("ix_ipo_issues_issuer_id", table_name="ipo_issues")
    op.drop_table("ipo_issues")
    op.drop_table("issuers")
