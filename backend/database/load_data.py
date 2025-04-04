"""
This file is used to load data from a dictionary of table names and list-of-dict records.
It updates existing records and inserts new ones.

The data is loaded from the endpoints instead of Excel files,
and inserts the results into the database.
"""

import logging
import os
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from backend.scripts.audit_extractor import AuditDataExtractor
from backend.scripts.course_extractor import CourseDataExtractor
from backend.scripts.enrollment_extractor import EnrollmentDataExtractor
from .models import Instructor, Course, Offering, Requirement, Audit, CountsFor
from .models import Prereqs, CourseInstructor, Enrollment, Department
from .db import SessionLocal

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the centralized data directory
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))
os.makedirs(DATA_DIR, exist_ok=True)

tables = {
    "department": Department,
    "instructor": Instructor,
    "course": Course,
    "offering": Offering,
    "requirement": Requirement,
    "audit": Audit,
    "countsfor": CountsFor,
    "prereqs": Prereqs,
    "course_instructor": CourseInstructor,
    "enrollment": Enrollment,
}

primary_keys = {
    "department": ["dep_code"],
    "instructor": ["andrew_id"],
    "course": ["course_code"],
    "offering": ["offering_id"],
    "requirement": ["requirement"],
    "audit": ["audit_id"],
    "countsfor": ["course_code", "requirement"],
    "prereqs": ["course_code", "prerequisite", "group_id"],
    "course_instructor": ["andrew_id", "course_code"],
    "enrollment": ["enrollment_id"]
}

def load_data_from_dicts(data_dict: dict[str, list[dict]]) -> None:
    """
    Loads data from a dictionary of table names and list-of-dict records.
    Updates existing records and inserts new ones.
    """
    db: Session = SessionLocal()
    try:
        logging.info("Loading data from dictionaries...")

        for table_name, records in data_dict.items():
            logging.info("Processing table: %s with %d records", table_name, len(records))

            model = tables.get(table_name)
            if not model:
                continue
            if not records:
                continue

            df = pd.DataFrame(records).drop_duplicates()
            deduped_records = df.to_dict(orient="records")

            if table_name == "enrollment":
                for record in deduped_records:
                    record["class_"] = int(record["class_"])  # Convert to int if necessary
                    offering = db.query(Offering).filter(
                        Offering.course_code == record["course_code"],
                        Offering.semester == record["semester"]
                    ).first()

                    if offering:
                        record["offering_id"] = offering.offering_id

            try:
                keys = primary_keys.get(table_name, [])

                if keys:
                    for record in deduped_records:
                        filter_conditions = []
                        has_all_keys = True
                        for key in keys:
                            if key in record:
                                filter_conditions.append(getattr(model, key) == record[key])
                            else:
                                has_all_keys = False
                                break

                        if has_all_keys:
                            existing = db.query(model).filter(*filter_conditions).first()

                            if existing:
                                for key, value in record.items():
                                    setattr(existing, key, value)
                            else:
                                new_record = model(**record)
                                db.add(new_record)

                else:
                    db.bulk_insert_mappings(model, deduped_records)

                db.commit()

            except IntegrityError as error:
                db.rollback()
                logging.error("Integrity error processing %s: %s", table_name, error)
                raise
            except SQLAlchemyError as error:
                db.rollback()
                logging.error("SQLAlchemy error processing %s: %s", table_name, error)
                raise
            except ValueError as error:
                db.rollback()
                logging.error("Value error processing %s: %s", table_name, error)
                raise
            except Exception as error:
                db.rollback()
                logging.error("Unexpected error processing %s: %s", table_name, error)
                raise
    finally:
        db.close()
        logging.info("Finished data loading process")

def load_data_from_endpoint() -> None:
    """
    Loads data directly from the new extractor endpoints instead of Excel files,
    and inserts the results into the database.
    """
    audit_extractor = AuditDataExtractor(audit_base_path=os.path.join(DATA_DIR, "audit"),
                                          course_base_path=os.path.join(DATA_DIR, "course"))
    course_extractor = CourseDataExtractor(folder_path=os.path.join(DATA_DIR, "course/courses"),
                                            base_dir=os.path.join(DATA_DIR, "course"))
    enrollment_extractor = EnrollmentDataExtractor()

    audit_results = audit_extractor.get_results()
    course_results = course_extractor.get_results()
    enrollment_data = enrollment_extractor.extract_enrollment_data(
        file_path=os.path.join(DATA_DIR, "enrollment/Enrollment.xlsx"))

    logging.info("Audit extractor results: %s", audit_results)
    logging.info("Course extractor results: %s", course_results)
    logging.info("Enrollment data extracted: %s",
                 enrollment_data if enrollment_data else "No enrollment data")

    data_dict = {}
    data_dict.update(audit_results)
    data_dict.update(course_results)
    data_dict["enrollment"] = (enrollment_data if isinstance(enrollment_data, list) else [])

    try:
        dept_df = pd.read_csv(os.path.join(DATA_DIR, "department/departments.csv"))
        data_dict["department"] = dept_df.to_dict(orient="records")
    except FileNotFoundError as e:
        logging.error("Department data file not found: %s", e)
        data_dict["department"] = []
    except pd.errors.EmptyDataError as e:
        logging.error("Department data file is empty: %s", e)
        data_dict["department"] = []
    except Exception as e: # pylint: disable=broad-exception-caught
        logging.error("Unexpected error loading department data: %s", e)
        data_dict["department"] = []

    logging.info("Combined data to be loaded: %s", {k: len(v) for k, v in data_dict.items()})

    load_data_from_dicts(data_dict)

if __name__ == "__main__":
    load_data_from_endpoint()
