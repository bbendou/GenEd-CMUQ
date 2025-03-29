"""
this script contains data models used for API input validation and response serialization,
ensuring type safety and structure for course-related operations.
"""

from typing import Optional, Dict, List
from pydantic import BaseModel, Field

class CourseFilter(BaseModel):
    """
    represents the query parameters for filtering courses.
    """
    cs_requirement: Optional[str] = Field(None, description="CS requirement")
    is_requirement: Optional[str] = Field(None, description="IS requirement")
    ba_requirement: Optional[str] = Field(None, description="BA requirement")
    bs_requirement: Optional[str] = Field(None, description="BS requirement)")


class RequirementResponse(BaseModel):
    """Pydantic schema for a single requirement."""
    requirement: str
    type: bool
    major: str

class CourseResponse(BaseModel):
    """
    represents a single course.
    """
    course_code: str
    course_name: str
    department: str
    units: Optional[int] = None
    description: Optional[str] = None
    prerequisites: Optional[str] = "None"
    offered: List[str]
    offered_qatar: bool
    offered_pitts: bool
    # Now each major maps to a list of requirement objects
    requirements: Dict[str, List[RequirementResponse]]

class CourseListResponse(BaseModel):
    """
    represents a list of filtered courses.
    """
    courses: List[CourseResponse]


class RequirementsResponse(BaseModel):
    """Pydantic schema for returning a list of requirements."""
    requirements: List[RequirementResponse]

class DepartmentResponse(BaseModel):
    """Pydantic schema for a single department."""
    dep_code: str
    name: str

class DepartmentListResponse(BaseModel):
    """Represents a list of departments."""
    departments: List[DepartmentResponse]

class CourseCoverageItem(BaseModel):
    """Schema for individual requirement coverage."""
    requirement: str
    num_courses: int

class CourseCoverageResponse(BaseModel):
    """Schema for course coverage response."""
    major: str
    semester: Optional[str] = None
    coverage: List[CourseCoverageItem]

class CombinedCourseFilter(BaseModel):
    """Represents the query parameters for filtering courses."""
    searchQuery: Optional[str] = Field(None, description="Search course code")
    department: Optional[str] = Field(None, description="Filter by department code")
    semester: Optional[str] = Field(None, description="Filter by semester offered, e.g. 'Fall2025'")
    has_prereqs: Optional[bool] = Field(None, description="False to filter for courses with"
    " no prerequisites")
    cs_requirement: Optional[str] = Field(None, description="Filter by CS requirement")
    is_requirement: Optional[str] = Field(None, description="Filter by IS requirement")
    ba_requirement: Optional[str] = Field(None, description="Filter by BA requirement")
    bs_requirement: Optional[str] = Field(None, description="Filter by BS requirement")
    offered_qatar: Optional[bool] = Field(None, description="Filter by courses offered in Qatar")
    offered_pitts: Optional[bool] = Field(None, description="Filter by courses offered in "
    "Pittsburgh")
