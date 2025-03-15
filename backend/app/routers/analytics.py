from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# If you’re reading from Excel files, you won't necessarily need SQLAlchemy,
# but if you're using a DB, you'll import get_db and possibly a repository.
from backend.database.db import get_db
from backend.app.schemas import CoverageOut, PredictOut
from backend.services import analytics as analytics_service

router = APIRouter()


@router.get("/analytics/requirement-coverage", response_model=list[CoverageOut])
def get_requirement_coverage(db: Session = Depends(get_db)):
    """
    Returns data for the bar graph (based on Countsfor.xlsx & Requirement.xlsx)
    OR from your DB tables if you migrated data there.
    """
    try:
        coverage_data = analytics_service.get_requirement_coverage(db)
        return coverage_data
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/analytics/predict", response_model=PredictOut)
def predict_course_offering(
    course_code: str,
    target_semester: str,
    db: Session = Depends(get_db)
):
    """
    Predicts if a course is offered in a given semester (based on Offering.xlsx)
    OR from your DB tables if that data is in the 'offering' table.
    Example usage: /analytics/predict?course_code=CS101&target_semester=S26
    """
    try:
        return analytics_service.predict_course_offering(db, course_code, target_semester)
    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
