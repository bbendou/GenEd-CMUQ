"""
this script implements the data access layer for courses.
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from backend.database.models import Course, CountsFor, Requirement, Offering

class CourseRepository:
    """encapsulates all database operations for the 'Course' entity."""

    def __init__(self, db: Session):
        self.db = db

    def get_course_by_code(self, course_code: str):
        """fetch course details by course code (raw data only)."""
        return self.db.query(Course).filter(Course.course_code == course_code).first()

    def get_all_courses(self):
        """fetch all courses with full details including units and description."""
        courses = self.db.query(
            Course.course_code,
            Course.name,
            Course.dep_code,
            Course.units,
            Course.description,
            Course.prereqs_text
        ).all()

        result = []
        for course in courses:
            offered_semesters = self.get_offered_semesters(course.course_code)
            requirements = self.get_course_requirements(course.course_code)

            result.append({
                "course_code": course.course_code,
                "course_name": course.name,
                "department": course.dep_code,
                "units": course.units,
                "description": course.description,
                "prerequisites": course.prereqs_text or "None",
                "offered": offered_semesters,
                "requirements": requirements,
            })

        return result

    def get_courses_by_department(self, department: str):
        """fetch all courses within a department with full details."""
        courses = self.db.query(
            Course.course_code,
            Course.name,
            Course.dep_code,
            Course.units,
            Course.description,
            Course.prereqs_text
        ).filter(Course.dep_code == department).all()

        result = []
        for course in courses:
            offered_semesters = self.get_offered_semesters(course.course_code)
            requirements = self.get_course_requirements(course.course_code)

            result.append({
                "course_code": course.course_code,
                "course_name": course.name,
                "department": course.dep_code,
                "units": course.units,
                "description": course.description,
                "prerequisites": course.prereqs_text or "None",
                "offered": offered_semesters,
                "requirements": requirements,
            })

        return result

    def get_offered_semesters(self, course_code: str):
        """fetch semesters in which a course is offered."""
        offered_semesters = (
            self.db.query(Offering.semester)
            .filter(Offering.course_code == course_code)
            .all()
        )
        return [semester[0] for semester in offered_semesters]

    def get_course_requirements(self, course_code: str):
        """fetch requirements per major for a course."""
        requirements = {"CS": [], "IS": [], "BA": [], "BS": []}
        requirements_query = (
            self.db.query(CountsFor.requirement, Requirement.audit_id)
            .join(Requirement, CountsFor.requirement == Requirement.requirement)
            .filter(CountsFor.course_code == course_code)
            .all()
        )

        print(f"DEBUG: Course {course_code} requirements: {requirements_query}")  # 🔍 Debugging

        for req, audit_id in requirements_query:
            if audit_id.startswith("cs"):
                requirements["CS"].append(req)
            elif audit_id.startswith("is"):
                requirements["IS"].append(req)
            elif audit_id.startswith("ba"):
                requirements["BA"].append(req)
            elif audit_id.startswith("bio"):
                requirements["BS"].append(req)

        print(f"DEBUG: Transformed requirements: {requirements}")  # 🔍 Debugging

        return requirements


    def get_courses_by_requirement(self, cs_requirement=None, is_requirement=None,
                                   ba_requirement=None, bs_requirement=None):
        """fetch courses that match all specified major requirements (AND filtering)."""
        filters = []
        if cs_requirement:
            filters.append(and_(Requirement.audit_id.like("cs%"),
                                 CountsFor.requirement == cs_requirement))
        if is_requirement:
            filters.append(and_(Requirement.audit_id.like("is%"),
                                CountsFor.requirement == is_requirement))
        if ba_requirement:
            filters.append(and_(Requirement.audit_id.like("ba%"),
                                CountsFor.requirement == ba_requirement))
        if bs_requirement:
            filters.append(and_(Requirement.audit_id.like("bio%"),
                                CountsFor.requirement == bs_requirement))

        if not filters:
            return []

        query = (
            self.db.query(Course.course_code, Course.name, Course.dep_code,
                          Course.prereqs_text, CountsFor.requirement, Requirement.audit_id)
            .join(CountsFor, Course.course_code == CountsFor.course_code)
            .join(Requirement, CountsFor.requirement == Requirement.requirement)
            .filter(or_(*filters))
        )

        return query.all()

    def get_courses_by_prerequisite(self, has_prereqs: bool):
        """fetch courses that either have or do not have prerequisites with full details."""

        if has_prereqs:
            query = self.db.query(
                Course.course_code,
                Course.name,
                Course.dep_code,
                Course.units,
                Course.description,
                Course.prereqs_text
            ).filter(Course.prereqs_text.isnot(None), Course.prereqs_text != "")
        else:
            query = self.db.query(
                Course.course_code,
                Course.name,
                Course.dep_code,
                Course.units,
                Course.description,
                Course.prereqs_text
            ).filter((Course.prereqs_text.is_(None)) | (Course.prereqs_text == ""))

        courses = query.all()

        result = []
        for course in courses:
            offered_semesters = self.get_offered_semesters(course.course_code)
            requirements = self.get_course_requirements(course.course_code)

            result.append({
                "course_code": course.course_code,
                "course_name": course.name,
                "department": course.dep_code,
                "units": course.units,  # ✅ Fix: Include units
                "description": course.description,  # ✅ Fix: Include description
                "prerequisites": course.prereqs_text if has_prereqs else "None",
                "offered": offered_semesters,
                "requirements": requirements,
            })

        return result



    def get_all_departments(self):
        """fetch all unique departments from the database."""
        departments = self.db.query(Course.dep_code).distinct().all()
        return [dept[0] for dept in departments]
