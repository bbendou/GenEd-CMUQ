"""
This script defines API endpoints for course-related operations.
This module contains the FastAPI routes for retrieving course information,
filtering courses based on department and requirements, and integrating with
the service layer for business logic.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.services.courses import CourseService
from backend.services import courses as courses_free  # Free functions for majors, semesters, analytics
from backend.app.schemas import (
    CourseResponse,
    CourseListResponse,
    CourseFilter,
    DepartmentListResponse,
    AnalyticsOut,
    PredictOut,
)

router = APIRouter()


def get_course_service(db: Session = Depends(get_db)) -> CourseService:
    """
    Provides a CourseService instance for handling course-related operations.
    """
    return CourseService(db)


@router.get("/courses", response_model=CourseListResponse)
def get_all_courses(course_service: CourseService = Depends(get_course_service)):
    """
    API route to fetch all courses.
    """
    return course_service.fetch_all_courses()


@router.get("/courses/by-department", response_model=CourseListResponse)
def get_courses_by_department_route(
    department: str, course_service: CourseService = Depends(get_course_service)
):
    """
    Fetch courses filtered by department.
    """
    return course_service.fetch_courses_by_department(department)


@router.get("/courses/filter", response_model=CourseListResponse)
def get_courses_by_requirement_route(
    course_filter: CourseFilter = Depends(),
    course_service: CourseService = Depends(get_course_service)
):
    """
    Fetch courses based on specified major requirements.
    """
    courses = course_service.fetch_courses_by_requirement(
        course_filter.cs_requirement,
        course_filter.is_requirement,
        course_filter.ba_requirement,
        course_filter.bs_requirement,
    )

    if not courses.courses:
        raise HTTPException(
            status_code=404,
            detail="No courses found matching the selected requirements",
        )

    return courses


@router.get("/courses/by-prerequisite", response_model=CourseListResponse)
def get_courses_by_prerequisite(
    has_prereqs: bool,
    course_service: CourseService = Depends(get_course_service)
):
    """
    Fetch courses based on whether they have prerequisites.
    Example usage:
      - `/courses/by-prerequisite?has_prereqs=true` → Fetch courses with prerequisites.
      - `/courses/by-prerequisite?has_prereqs=false` → Fetch courses without prerequisites.
    """
    return course_service.fetch_courses_by_prerequisite(has_prereqs)


@router.get("/courses/{course_code}", response_model=CourseResponse)
def get_course(course_code: str, course_service: CourseService = Depends(get_course_service)):
    """
    Fetch course details by course code.
    """
    course = course_service.fetch_course_by_code(course_code)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.get("/departments", response_model=DepartmentListResponse)
def get_departments(course_service: CourseService = Depends(get_course_service)):
    """
    API route to fetch all available departments.
    """
    return DepartmentListResponse(departments=course_service.fetch_all_departments())


# New endpoints for analytics based on the guidelines
@router.get("/majors", response_model=List[str])
async def get_majors():
    """
    Returns a list of available majors.
    """
    majors = courses_free.get_majors()
    if not majors:
        raise HTTPException(status_code=404, detail="No majors found")
    return majors


@router.get("/semesters", response_model=List[str])
async def get_semesters():
    """
    Returns a list of available semesters.
    """
    semesters = courses_free.get_semesters()
    if not semesters:
        raise HTTPException(status_code=404, detail="No semesters found")
    return semesters


@router.get("/analytics", response_model=List[AnalyticsOut])
async def get_analytics(major: str, semester: str):
    """
    Returns analytics data for a given major and semester.
    Data is aggregated to show the number of distinct course offerings per requirement.
    """
    analytics_data = courses_free.get_analytics(major, semester)
    if analytics_data is None or len(analytics_data) == 0:
        raise HTTPException(status_code=404, detail="No analytics data found")
    return analytics_data


@router.get("/predict", response_model=PredictOut)
async def predict_course_offering_endpoint(
    course_code: str, target_semester: str, db: Session = Depends(get_db)
):
    """
    Predicts if a course is offered in a given semester.
    Example usage: GET /courses/predict?course_code=15-110&target_semester=F22
    """
    try:
        # Use the free function from courses_free for prediction
        prediction = courses_free.get_prediction(course_code, target_semester)
        if not prediction:
            raise HTTPException(status_code=404, detail="Prediction not found")
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
