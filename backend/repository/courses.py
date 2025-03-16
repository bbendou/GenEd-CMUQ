"""
this script implements the data access layer for courses.
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from backend.database.models import Course, CountsFor, Requirement, Offering, Audit
from backend.app.utils import semester_sort_key
from backend.database.db import get_db


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


def get_all_majors():
    """
    Query the Audit table for distinct majors.
    """
    session: Session = next(get_db())
    try:
        results = session.query(Audit.major).distinct().all()
        majors = [row[0] for row in results if row[0] is not None]
        return majors
    finally:
        session.close()

def get_all_semesters():
    """
    Query the Offering table for distinct semesters.
    """
    session: Session = next(get_db())
    try:
        results = session.query(Offering.semester).distinct().all()
        semesters = [row[0] for row in results if row[0] is not None]
        return semesters
    finally:
        session.close()

def get_analytics_data(major: str, semester: str):
    """
    Aggregates analytics data by counting distinct courses for each requirement,
    for a given major (from Audit.major) and semester (from Offering.semester).

    Joins:
      - Requirement joined with Audit (via audit_id) to filter by major.
      - Requirement joined with CountsFor (on requirement).
      - CountsFor joined with Course (on course_code).
      - Course joined with Offering (on course_code) to filter by semester.
    """
    session: Session = next(get_db())
    try:
        results = (
            session.query(
                Requirement.requirement,
                func.count(func.distinct(Course.course_code)).label("NumCourses")
            )
            .join(Audit, Requirement.audit_id == Audit.audit_id)
            .join(CountsFor, Requirement.requirement == CountsFor.requirement)
            .join(Course, CountsFor.course_code == Course.course_code)
            .join(Offering, Course.course_code == Offering.course_code)
            .filter(Audit.major == major, Offering.semester == semester)
            .group_by(Requirement.requirement)
            .all()
        )
        analytics = []
        for requirement_text, num_courses in results:
            short_requirement = requirement_text.split('---')[-1].strip() if requirement_text else ""
            analytics.append({
                "major": major,
                "short_requirement": short_requirement,
                "NumCourses": num_courses
            })
        return analytics
    finally:
        session.close()

def get_prediction_data(course_code: str, target_semester: str):
    """
    Reads the Offering.xlsx file and applies rule-based logic to determine
    if the given course is likely to be offered in the target semester.
    """
    import os
    import pandas as pd

    # Adjust the path to go from repository to the data folder
    data_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "course")
    offering_file = os.path.join(data_dir, "Offering.xlsx")

    df = pd.read_excel(offering_file, engine="openpyxl")
    df.columns = df.columns.str.strip()
    df["Offered"] = 1

    grouped = df.groupby(["course_code", "semester"])["Offered"].max().reset_index()
    unique_semesters = grouped["semester"].unique()
    # Ensure you have the semester_sort_key imported or defined here
    from backend.app.utils import semester_sort_key  # if you put it in a utils module
    sorted_semesters = sorted(unique_semesters, key=semester_sort_key)

    wide_data = grouped.pivot(index="course_code", columns="semester", values="Offered")
    wide_data = wide_data.reindex(columns=sorted_semesters, fill_value=0).reset_index()
    wide_data.columns.name = None
    wide_data = wide_data.fillna(0)

    # Locate row for the course
    course_row = wide_data[wide_data["course_code"] == course_code]
    if course_row.empty:
        return {
            "course_code": course_code,
            "target_semester": target_semester,
            "prediction": "NO_DATA",
            "reason": f"Course {course_code} not found in data."
        }

    target_season = target_semester[0].upper()  # e.g., "F", "S", or "M"
    season_cols = [
        col for col in sorted_semesters
        if col.startswith(target_season) and int(col[1:]) > 20
    ]

    offered_values = []
    for col in season_cols:
        if col in course_row.columns:
            offered_values.append(int(course_row[col].iloc[0]))
        else:
            offered_values.append(0)

    fraction_offered = sum(offered_values) / len(offered_values) if offered_values else 0
    threshold = 0.5
    prediction = "YES" if fraction_offered >= threshold else "NO"

    return {
        "course_code": course_code,
        "target_semester": target_semester,
        "prediction": prediction,
        "fraction_offered": fraction_offered
    }