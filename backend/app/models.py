from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def new_uuid() -> str:
    return str(uuid4())


class ResearchCase(Base):
    __tablename__ = "research_cases"
    __table_args__ = (
        CheckConstraint("case_status IN ('identity_pending', 'active', 'archived')", name="ck_research_cases_status"),
        CheckConstraint(
            "identity_status IN ('unresolved', 'ambiguous', 'confirmed', 'out_of_scope', 'rejected')",
            name="ck_research_cases_identity_status",
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    entered_name: Mapped[str] = mapped_column(String(200), nullable=False)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    case_status: Mapped[str] = mapped_column(String(32), nullable=False, default="identity_pending", index=True)
    identity_status: Mapped[str] = mapped_column(String(32), nullable=False, default="unresolved")
    issue_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("ipo_issues.id"), nullable=True)
    created_at: Mapped[str] = mapped_column(String(40), nullable=False, default=utc_now)
    updated_at: Mapped[str] = mapped_column(String(40), nullable=False, default=utc_now, onupdate=utc_now)
    last_activity_at: Mapped[str] = mapped_column(String(40), nullable=False, default=utc_now, index=True)
    latest_analysis_run_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    latest_report_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    case_changed_since_last_run: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    readiness_summary: Mapped[str | None] = mapped_column(String(16), nullable=True)
    warning_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class EvidenceItem(Base):
    __tablename__ = "evidence_items"
    __table_args__ = (
        CheckConstraint("evidence_kind IN ('web_page', 'manual_note', 'manual_value', 'document')", name="ck_evidence_items_kind"),
        CheckConstraint("verification_status IN ('unverified', 'reviewed', 'rejected', 'superseded')", name="ck_evidence_items_verification"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    case_id: Mapped[str] = mapped_column(String(36), ForeignKey("research_cases.id"), nullable=False, index=True)
    evidence_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    source_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    original_file_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    mime_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    size_bytes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sha256: Mapped[str | None] = mapped_column(String(64), nullable=True)
    published_at: Mapped[str | None] = mapped_column(String(40), nullable=True)
    captured_at: Mapped[str] = mapped_column(String(40), nullable=False, default=utc_now, index=True)
    locator: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    verification_status: Mapped[str] = mapped_column(String(24), nullable=False, default="unverified")
    notes: Mapped[str | None] = mapped_column(String, nullable=True)
    local_relative_path: Mapped[str | None] = mapped_column(String(500), nullable=True)


class Issuer(Base):
    __tablename__ = "issuers"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    legal_name: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[str] = mapped_column(String(40), nullable=False, default=utc_now)
    updated_at: Mapped[str] = mapped_column(String(40), nullable=False, default=utc_now, onupdate=utc_now)


class IpoIssue(Base):
    __tablename__ = "ipo_issues"
    __table_args__ = (
        CheckConstraint("market_segment = 'MAINBOARD'", name="ck_ipo_issues_mainboard_only"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    issuer_id: Mapped[str] = mapped_column(String(36), ForeignKey("issuers.id"), nullable=False, index=True)
    display_name: Mapped[str] = mapped_column(String(200), nullable=False)
    market_segment: Mapped[str] = mapped_column(String(16), nullable=False, default="MAINBOARD")
    open_date: Mapped[str | None] = mapped_column(String(10), nullable=True)
    close_date: Mapped[str | None] = mapped_column(String(10), nullable=True)
    listing_date: Mapped[str | None] = mapped_column(String(10), nullable=True)
    price_band_low: Mapped[str | None] = mapped_column(String(64), nullable=True)
    price_band_high: Mapped[str | None] = mapped_column(String(64), nullable=True)
    issue_size_amount: Mapped[str | None] = mapped_column(String(64), nullable=True)
    issue_size_unit: Mapped[str | None] = mapped_column(String(32), nullable=True)
    created_at: Mapped[str] = mapped_column(String(40), nullable=False, default=utc_now)
    updated_at: Mapped[str] = mapped_column(String(40), nullable=False, default=utc_now, onupdate=utc_now)


class MarketObservation(Base):
    __tablename__ = "market_observations"
    __table_args__ = (
        CheckConstraint("signal_category IN ('issue_terms', 'company_financials', 'valuation', 'subscription_qib', 'subscription_nii', 'subscription_retail', 'gmp', 'market_context', 'company_events')", name="ck_market_observations_signal_category"),
        CheckConstraint("review_status IN ('candidate', 'accepted', 'rejected', 'conflicted', 'superseded')", name="ck_market_observations_review_status"),
        CheckConstraint("entry_method IN ('manual', 'extracted_candidate', 'imported', 'connector', 'derived')", name="ck_market_observations_entry_method"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    case_id: Mapped[str] = mapped_column(String(36), ForeignKey("research_cases.id"), nullable=False, index=True)
    indicator_code: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    signal_category: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    segment: Mapped[str | None] = mapped_column(String(16), nullable=True)
    raw_value_text: Mapped[str] = mapped_column(String(5000), nullable=False)
    value_numeric: Mapped[str | None] = mapped_column(String(64), nullable=True)
    value_text: Mapped[str | None] = mapped_column(String(5000), nullable=True)
    unit: Mapped[str | None] = mapped_column(String(64), nullable=True)
    currency: Mapped[str | None] = mapped_column(String(8), nullable=True)
    metric_definition: Mapped[str] = mapped_column(String(2000), nullable=False)
    observed_at: Mapped[str | None] = mapped_column(String(40), nullable=True)
    published_at: Mapped[str | None] = mapped_column(String(40), nullable=True)
    retrieved_at: Mapped[str | None] = mapped_column(String(40), nullable=True)
    recorded_at: Mapped[str] = mapped_column(String(40), nullable=False, default=utc_now)
    source_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    acquisition_attempt_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    evidence_id: Mapped[str] = mapped_column(String(36), ForeignKey("evidence_items.id"), nullable=False, index=True)
    entry_method: Mapped[str] = mapped_column(String(24), nullable=False, default="manual")
    review_status: Mapped[str] = mapped_column(String(24), nullable=False, default="candidate", index=True)
    definition_metadata_json: Mapped[str] = mapped_column(String, nullable=False, default="{}")
    reviewed_at: Mapped[str | None] = mapped_column(String(40), nullable=True)
    review_rationale: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    supersedes_observation_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
