"""
This script contains the business logic for handling courses.
"""

from typing import Dict, Optional
from sqlalchemy.orm import Session
from backend.repository.courses import CourseRepository
from backend.repository import courses as courses_repo
from backend.app.schemas import CourseResponse, CourseListResponse


class CourseService:
    """encapsulates business logic for handling courses."""

    def __init__(self, db: Session):
        self.course_repo = CourseRepository(db)

    def fetch_course_by_code(self, course_code: str) -> Optional[CourseResponse]:
        """fetch a course and format its response."""
        course = self.course_repo.get_course_by_code(course_code)
        if not course:
            return None

        return CourseResponse(
            course_code=course.course_code,
            course_name=course.name,
            department=course.dep_code,
            units=course.units,
            description=course.description,
            prerequisites=course.prereqs_text or "None",
            offered=self.course_repo.get_offered_semesters(course_code),
            offered_qatar=course.offered_qatar,
            offered_pitts=course.offered_pitts,
            requirements=self.course_repo.get_course_requirements(course_code),
        )

    def fetch_all_courses(self) -> CourseListResponse:
        """fetch and structure all courses, prioritizing those fulfilling at l
        east one requirement."""
        courses = self.course_repo.get_all_courses()

        for course in courses:
            course["num_requirements"] = sum(len(reqs) for reqs in course["requirements"].values())
            course["num_offered_semesters"] = len(course["offered"])

        sorted_courses = sorted(
            courses,
            key=lambda c: (c["num_requirements"] == 0, -c["num_offered_semesters"]),
            reverse=False
        )

        return CourseListResponse(
            courses=[
                CourseResponse(
                    course_code=course["course_code"],
                    course_name=course["course_name"],
                    department=course["department"],
                    units=course["units"],
                    description=course["description"],
                    prerequisites=course["prerequisites"],
                    offered=course["offered"],
                    offered_qatar=course["offered_qatar"],
                    offered_pitts=course["offered_pitts"],
                    requirements=course["requirements"],
                )
                for course in sorted_courses
            ]
        )

    def fetch_courses_by_requirement(self, cs_requirement=None,
                                     is_requirement=None,
                                     ba_requirement=None,
                                     bs_requirement=None) -> CourseListResponse:
        """fetch and process courses matching requirements."""
        raw_results = self.course_repo.get_courses_by_requirement(cs_requirement, is_requirement,
                                                                  ba_requirement, bs_requirement)

        course_dict: Dict[str, dict] = {}
        for (course_code, course_name, department,
             prerequisites, requirement, audit_id) in raw_results:
            if course_code not in course_dict:
                course_dict[course_code] = {
                    "course_code": course_code,
                    "course_name": course_name,
                    "department": department,
                    "prerequisites": prerequisites or "None",
                    "offered": self.course_repo.get_offered_semesters(course_code),
                    "requirements": {"CS": [], "IS": [], "BA": [], "BS": []},
                }

            if audit_id.startswith("cs"):
                course_dict[course_code]["requirements"]["CS"].append(requirement)
            elif audit_id.startswith("is"):
                course_dict[course_code]["requirements"]["IS"].append(requirement)
            elif audit_id.startswith("ba"):
                course_dict[course_code]["requirements"]["BA"].append(requirement)
            elif audit_id.startswith("bio"):
                course_dict[course_code]["requirements"]["BS"].append(requirement)

        return CourseListResponse(
            courses=[CourseResponse(**course) for course in course_dict.values()]
        )

    def fetch_courses_by_prerequisite(self, has_prereqs: bool) -> CourseListResponse:
        """fetch and structure courses based on whether they have prerequisites."""
        courses = self.course_repo.get_courses_by_prerequisite(has_prereqs)

        return CourseListResponse(
            courses=[
                CourseResponse(
                    course_code=course["course_code"],
                    course_name=course["course_name"],
                    department=course["department"],
                    units=course["units"],
                    description=course["description"],
                    prerequisites=course["prerequisites"],
                    offered=course["offered"],
                    offered_qatar=course["offered_qatar"],
                    offered_pitts=course["offered_pitts"],
                    requirements=course["requirements"],
                )
                for course in courses
            ]
        )

    def fetch_courses_by_department(self, department: str) -> CourseListResponse:
        """fetch and structure courses filtered by department."""
        courses = self.course_repo.get_courses_by_department(department)

        return CourseListResponse(
            courses=[
                CourseResponse(
                    course_code=course["course_code"],
                    course_name=course["course_name"],
                    department=course["department"],
                    units=course["units"],
                    description=course["description"],
                    prerequisites=course["prerequisites"],
                    offered=course["offered"],
                    offered_qatar=course["offered_qatar"],
                    offered_pitts=course["offered_pitts"],
                    requirements=course["requirements"],
                )
                for course in courses
            ]
        )

    def fetch_courses_by_offered_location(self, offered_in_qatar: bool,
                                          offered_in_pitts: bool) -> CourseListResponse:
        """fetch and process courses filtered by offering location."""
        raw_courses = self.course_repo.get_courses_by_offered_location(offered_in_qatar,
                                                                       offered_in_pitts)
        return CourseListResponse(
            courses=[
                CourseResponse(
                    course_code=c["course_code"],
                    course_name=c["course_name"],
                    department=c["department"],
                    units=c["units"],
                    description=c["description"],
                    prerequisites=c["prerequisites"],
                    offered=c["offered"],
                    offered_qatar=c["offered_qatar"],
                    offered_pitts=c["offered_pitts"],
                    requirements=c["requirements"],
                )
                for c in raw_courses
            ]
        )
    
    def get_enrollment(course_code: str, class_number: Optional[int] = None, sem: Optional[str] = None):
        """
        Retrieves enrollment data for a given course.
        This function calls the repository function to read from Enrollment.xlsx.
        """
        # Instantiate the repository. Since this function only reads from Excel,
        # we can pass None as the session.
        from backend.repository import courses as courses_repo
        repo = courses_repo.CourseRepository(None)
        return repo.get_enrollment_data(course_code, class_number, sem)
    
def get_majors():
    return courses_repo.get_all_majors()

def get_semesters():
    return courses_repo.get_all_semesters()

def get_analytics(major: str, semester: str):
    return courses_repo.get_analytics_data(major, semester)

def get_prediction(course_code: str, target_semester: str):
    return courses_repo.get_prediction_data(course_code, target_semester)

def get_enrollment(course_code: str, class_number: Optional[int] = None, sem: Optional[str] = None):
    """
    Retrieves enrollment data for a given course. Optionally filters by class_number and semester.
    This function instantiates a temporary CourseRepository (which reads directly from the Excel file)
    since enrollment data is not stored in the database.
    """
    # Since get_enrollment_data only reads from Excel, we pass None as the session.
    repo = courses_repo.CourseRepository(None)
    return repo.get_enrollment_data(course_code, class_number, sem)


