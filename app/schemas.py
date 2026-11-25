"""Schemas for structured data extracted from job postings.

Convention: any field not stated in the posting is left as None (or an empty
list). Extraction should never guess values that aren't in the text.
"""

from __future__ import annotations

from datetime import date
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class WorkMode(str, Enum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ONSITE = "onsite"


class EmploymentType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"


class PayPeriod(str, Enum):
    HOUR = "hour"
    MONTH = "month"
    YEAR = "year"


class Compensation(BaseModel):
    min_amount: float | None = Field(None, description="Lower bound of the pay range.")
    max_amount: float | None = Field(
        None, description="Upper bound. For 'up to X', only max_amount is set."
    )
    currency: str | None = Field(None, description="ISO 4217 code, e.g. USD, EUR, GBP, CAD.")
    period: PayPeriod | None = None
    extras: list[str] = Field(
        default_factory=list,
        description="Non-base pay, e.g. 'equity', '10% bonus', 'RSUs', '$3,000 housing stipend'.",
    )


class Contact(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None


class JobPosting(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(..., description="Job title as written, e.g. 'Senior Backend Engineer'.")
    company: str | None = Field(None, description="Hiring company; None if not named (e.g. recruiter outreach).")
    locations: list[str] = Field(
        default_factory=list, description="Cities/regions as written, e.g. ['Austin, TX']."
    )
    work_mode: WorkMode | None = None
    remote_restrictions: str | None = Field(
        None, description="Constraints on remote work, e.g. 'US only', 'EU', 'overlap 4h with US Eastern'."
    )
    employment_type: EmploymentType | None = None
    contract_duration: str | None = Field(None, description="For contracts/internships, e.g. '6 months'.")
    compensation: Compensation | None = None

    min_years_experience: int | None = Field(
        None, description="Lower bound of required experience, e.g. '5+ years' -> 5, '4-6 yrs' -> 4."
    )
    responsibilities: list[str] = Field(default_factory=list)
    requirements: list[str] = Field(default_factory=list, description="Must-have qualifications.")
    nice_to_have: list[str] = Field(default_factory=list, description="Preferred / bonus qualifications.")
    benefits: list[str] = Field(default_factory=list)
    visa_sponsorship: bool | None = None

    apply_url: str | None = None
    apply_email: str | None = None
    deadline: date | None = Field(None, description="Application deadline, if stated.")
    start_date: str | None = Field(None, description="As written, e.g. 'ASAP', 'early January'.")
    contact: Contact | None = Field(None, description="Recruiter or hiring contact, if named.")
