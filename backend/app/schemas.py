"""
This script contains data models used for API input validation
and response serialization, ensuring type safety and structure
for course-related operations.
"""

from typing import Optional, Dict, List
from pydantic import BaseModel, Field


class CourseFilter(BaseModel):
    """
    Represents the query parameters for filtering courses.
    """
    cs_requirement: Optional[str] = Field(None, description="CS requirement")
    is_requirement: Optional[str] = Field(None, description="IS requirement")
    ba_requirement: Optional[str] = Field(None, description="BA requirement")
    bs_requirement: Optional[str] = Field(None, description="BS requirement)")


class CourseResponse(BaseModel):
    """
    Pydantic schema for a single course response.
    """
    course_code: str
    course_name: str
    department: str
    units: Optional[int] = None
    description: Optional[str] = None
    prerequisites: Optional[str] = "None"
    offered: List[str]
    requirements: Dict[str, List[str]]


class CourseListResponse(BaseModel):
    """
    Represents a list of filtered courses.
    """
    courses: List[CourseResponse]


class RequirementResponse(BaseModel):
    """
    Pydantic schema for a single requirement.
    """
    requirement: str
    type: bool
    major: str


class RequirementsResponse(BaseModel):
    """
    Pydantic schema for returning a list of requirements.
    """
    requirements: List[RequirementResponse]


class DepartmentListResponse(BaseModel):
    """
    Pydantic schema for returning a list of departments.
    """
    departments: List[str]


class CoverageOut(BaseModel):
    """
    Represents the coverage data for bar graph analytics.
    """
    major: Optional[str]
    short_requirement: str
    NumCourses: int


class PredictOut(BaseModel):
    """
    Schema for returning the result of the predictive model.
    """
    course_code: str
    target_semester: str
    prediction: str
    fraction_offered: Optional[float] = None
