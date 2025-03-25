"""
This script implements the data access layer for courses.
"""
from typing import Optional
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
        """fetch all courses with full details including units, description, and locations."""
        courses = self.db.query(
            Course.course_code,
            Course.name,
            Course.dep_code,
            Course.units,
            Course.description,
            Course.offered_qatar,
            Course.offered_pitts,
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
                "offered_qatar": course.offered_qatar,
                "offered_pitts": course.offered_pitts,
                "offered": offered_semesters,
                "requirements": requirements,
            })

        return result

    def get_courses_by_department(self, department: str):
        """fetch all courses within a department with full details."""
        courses = self.db.query(Course).filter(Course.dep_code == department).all()

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
                "offered_qatar": course.offered_qatar,
                "offered_pitts": course.offered_pitts,
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

        for req, audit_id in requirements_query:
            if audit_id.startswith("cs"):
                requirements["CS"].append(req)
            elif audit_id.startswith("is"):
                requirements["IS"].append(req)
            elif audit_id.startswith("ba"):
                requirements["BA"].append(req)
            elif audit_id.startswith("bio"):
                requirements["BS"].append(req)

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
        """fetch courses that either have or do not have prerequisites."""
        query = self.db.query(Course).filter(
            (Course.prereqs_text.isnot(None) & (Course.prereqs_text != "")) if has_prereqs else
            ((Course.prereqs_text.is_(None)) | (Course.prereqs_text == ""))
        )

        result = []
        for course in query.all():
            offered_semesters = self.get_offered_semesters(course.course_code)
            requirements = self.get_course_requirements(course.course_code)

            result.append({
                "course_code": course.course_code,
                "course_name": course.name,
                "department": course.dep_code,
                "units": course.units,
                "description": course.description,
                "prerequisites": course.prereqs_text if has_prereqs else "None",
                "offered_qatar": course.offered_qatar,
                "offered_pitts": course.offered_pitts,
                "offered": offered_semesters,
                "requirements": requirements,
            })

        return result

    def get_courses_by_offered_location(self, offered_in_qatar: bool, offered_in_pitts: bool):
        """fetch courses filtered by offering in Qatar and/or Pittsburgh."""
        query = self.db.query(Course)

        # Apply AND conditions based on input
        if offered_in_qatar is not None:
            query = query.filter(Course.offered_qatar == offered_in_qatar)
        if offered_in_pitts is not None:
            query = query.filter(Course.offered_pitts == offered_in_pitts)

        result = []
        for course in query.all():
            offered_semesters = self.get_offered_semesters(course.course_code)
            requirements = self.get_course_requirements(course.course_code)

            result.append({
                "course_code": course.course_code,
                "course_name": course.name,
                "department": course.dep_code,
                "units": course.units,
                "description": course.description,
                "prerequisites": course.prereqs_text or "None",
                "offered_qatar": course.offered_qatar,
                "offered_pitts": course.offered_pitts,
                "offered": offered_semesters,
                "requirements": requirements,
            })

        return result
    
    def get_enrollment_data(self, course_code: str, class_number: Optional[int] = None, sem: Optional[str] = None):
        """
        Reads enrollment data from Enrollment.xlsx, filters by course_code,
        and optionally by class_number and semester.
        Aggregates total enrollment by semester (or by semester and class if class_number is provided).
        """
        import os
        import pandas as pd

        # Build the absolute path to the enrollment data file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, "..", "..", "data", "enrollment")
        enrollment_file = os.path.join(data_dir, "Enrollment.xlsx")
        
        try:
            df = pd.read_excel(enrollment_file, engine="openpyxl")
        except Exception as e:
            raise Exception(f"Error reading enrollment file: {e}")

        df.columns = df.columns.str.strip()

        # Filter the DataFrame for the given course code
        df_course = df[df["course_code"] == course_code]
        if class_number is not None:
            df_course = df_course[df_course["class"] == class_number]
        if sem is not None:
            df_course = df_course[df_course["semester"] == sem]

        if df_course.empty:
            return []

        # If class_number is not provided, group by semester only;
        # otherwise, group by both semester and class.
        if class_number is None:
            grouped = df_course.groupby("semester")["enrollment_count"].sum().reset_index()
        else:
            grouped = df_course.groupby(["semester", "class"])["enrollment_count"].sum().reset_index()

        return grouped.to_dict(orient="records")

