"""
this module contains the AnalyticsRepository class, which encapsulates
database operations for analytics-related queries.
"""

from typing import Optional
from sqlalchemy.orm import Session
from backend.database.models import CountsFor, Requirement, Offering, Course, Audit

class AnalyticsRepository:
    """encapsulates database operations for analytics-related queries."""

    def __init__(self, db: Session):
        self.db = db

    def get_course_coverage(self, major: str, semester: Optional[str] = None):
        """Fetch the count of courses fulfilling each requirement for a given major,
        optionally filtering by courses with an offering record in Qatar
        and by semester if provided."""

        # Base query for requirements
        requirement_counts = (
            self.db.query(Requirement.requirement)
            .join(CountsFor, CountsFor.requirement == Requirement.requirement)
            .join(Audit, Requirement.audit_id == Audit.audit_id)
            .filter(Audit.major == major)
            .distinct()
        ).all()

        result = {}

        for (req,) in requirement_counts:
            # Build a subquery for course codes with an offering record in Qatar.
            offering_subq = self.db.query(Offering.course_code).filter(Offering.campus_id == 2)
            if semester:
                offering_subq = offering_subq.filter(Offering.semester == semester)
            offering_subq = offering_subq.subquery()

            # Count courses that are linked to the requirement and have
            #  an offering record (from the subquery)
            course_count = (
                self.db.query(Course)
                .join(CountsFor)
                .filter(
                    CountsFor.requirement == req,
                    Course.course_code.in_(offering_subq)
                )
                .distinct(Course.course_code)
                .count()
            )
            result[req] = course_count

        return result
