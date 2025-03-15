import os
import pandas as pd
from sqlalchemy.orm import Session

# If you'd like to unify logic with your scripts:
# from backend.app.scripts.bargraph import generate_requirement_coverage
# from backend.app.scripts.predict_next_sem import predict_offering


def get_requirement_coverage(db: Session):
    """
    If using DB:
      - join 'CountsFor', 'Requirement', 'Audit' tables to compute coverage.
    If using Excel:
      - read from 'Countsfor.xlsx' & 'Requirement.xlsx', then merge & return list[dict].
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "..", "data", "audit")
    counts_path = os.path.join(data_dir, "Countsfor.xlsx")
    req_path = os.path.join(data_dir, "Requirement.xlsx")

    df_counts = pd.read_excel(counts_path, engine="openpyxl")
    df_reqs = pd.read_excel(req_path, engine="openpyxl")

    df_merged = pd.merge(df_counts, df_reqs, on="requirement", how="left")
    df_merged["major"] = df_merged["audit_id"].apply(
        lambda x: x.split("_")[0] if pd.notnull(x) else None
    )
    df_merged["short_requirement"] = df_merged["requirement"].apply(
        lambda x: x.split("---")[-1].strip()
    )

    grouped = (
        df_merged.groupby(["major", "short_requirement"])["course_code"]
        .nunique()
        .reset_index(name="NumCourses")
    )

    coverage_data = grouped.to_dict(orient="records")
    return coverage_data


def predict_course_offering(db: Session, course_code: str, target_semester: str):
    """
    If using DB:
      - Query 'Offering' or 'Enrollment' for past patterns.
    If using Excel:
      - read 'Offering.xlsx' & do rule-based logic (like predict_next_sem).
    """
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data", "course")
    offering_file = os.path.join(data_dir, "Offering.xlsx")

    df = pd.read_excel(offering_file, engine="openpyxl")
    df.columns = df.columns.str.strip()
    df["Offered"] = 1

    # Example pivot logic, threshold check, etc.
    # Return a dict that your Pydantic schema (PredictOut) can handle
    return {
        "course_code": course_code,
        "target_semester": target_semester,
        "prediction": "YES",  # or "NO"
    }
