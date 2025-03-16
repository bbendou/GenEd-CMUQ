# from sqlalchemy.orm import Session
# from backend.database.models import Course, CountsFor, Requirement, Offering, Audit
# from analytics.predict_next_sem import semester_sort_key
# import os
# import pandas as pd


# def predict_course_offering(db: Session, course_code: str, target_semester: str):
#     """
#     If using Excel:
#       - read from 'Offering.xlsx' and apply rule-based logic.
#     """
#     # Adjust relative path: go two levels up to repository root, then into data/course.
#     data_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "course")
#     offering_file = os.path.join(data_dir, "Offering.xlsx")

#     df = pd.read_excel(offering_file, engine="openpyxl")
#     df.columns = df.columns.str.strip()
#     df["Offered"] = 1

#     grouped = df.groupby(["course_code", "semester"])["Offered"].max().reset_index()
#     unique_semesters = grouped["semester"].unique()
#     sorted_semesters = sorted(unique_semesters, key=semester_sort_key)

#     wide_data = grouped.pivot(index="course_code", columns="semester", values="Offered")
#     wide_data = wide_data.reindex(columns=sorted_semesters, fill_value=0).reset_index()
#     wide_data.columns.name = None
#     wide_data = wide_data.fillna(0)

#     # Locate row for that course
#     course_row = wide_data[wide_data["course_code"] == course_code]
#     if course_row.empty:
#         return {
#             "course_code": course_code,
#             "target_semester": target_semester,
#             "prediction": "NO_DATA",
#             "reason": f"Course {course_code} not found in data."
#         }

#     target_season = target_semester[0].upper()  # "S", "F", or "M"
#     season_cols = [
#         col for col in sorted_semesters
#         if col.startswith(target_season) and int(col[1:]) > 20
#     ]

#     offered_values = []
#     for col in season_cols:
#         if col in course_row.columns:
#             offered_values.append(int(course_row[col].iloc[0]))
#         else:
#             offered_values.append(0)

#     fraction_offered = sum(offered_values) / len(offered_values) if offered_values else 0
#     threshold = 0.5
#     prediction = "YES" if fraction_offered >= threshold else "NO"

#     return {
#         "course_code": course_code,
#         "target_semester": target_semester,
#         "prediction": prediction,
#         "fraction_offered": fraction_offered
#     }
