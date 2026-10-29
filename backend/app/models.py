from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, CheckConstraint, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


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
    issue_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=utc_now, onupdate=utc_now)
    last_activity_at: Mapped[datetime] = mapped_column(nullable=False, default=utc_now, index=True)
    latest_analysis_run_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    latest_report_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    case_changed_since_last_run: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    readiness_summary: Mapped[str | None] = mapped_column(String(16), nullable=True)
    warning_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
