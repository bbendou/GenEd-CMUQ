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
        """fetch the count of courses fulfilling each requirement for a given major,
        optionally filtering by semester."""

        # Base query
        requirement_counts = (
            self.db.query(Requirement.requirement)
            .join(CountsFor, CountsFor.requirement == Requirement.requirement)
            .join(Course, Course.course_code == CountsFor.course_code)
            .join(Audit, Requirement.audit_id == Audit.audit_id)
            .join(Offering, Offering.course_code == Course.course_code)
            .filter(Audit.major == major, Course.offered_qatar)
            .distinct()
        )

        if semester:
            requirement_counts = requirement_counts.filter(Offering.semester == semester)

        requirement_counts = requirement_counts.all()
        result = {}
        for (req,) in requirement_counts:
            course_query = self.db.query(Course).join(CountsFor).join(Offering).filter(
                CountsFor.requirement == req,
                Course.offered_qatar
            )
            if semester:
                course_query = course_query.filter(Offering.semester == semester)
            result[req] = course_query.count()


        return result
