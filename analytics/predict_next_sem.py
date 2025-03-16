# import os
# import pandas as pd
# import numpy as np


# def semester_sort_key(sem):
#     """
#     Sort a semester code based on an academic cycle:
#       - For Fall (F): effective_year = int(year), order = 0.
#       - For Spring (S) and Summer (M): effective_year = int(year) - 1,
#         order = 1 for Spring, 2 for Summer.
#     For example:
#       F20 -> (20, 0)
#       S21 -> (20, 1)
#       M21 -> (20, 2)
#       F21 -> (21, 0)
#     """
#     letter = sem[0].upper()
#     try:
#         year = int(sem[1:])
#     except Exception:
#         year = 0

#     if letter == "F":
#         effective_year = year
#         order = 0
#     elif letter == "S":
#         effective_year = year - 1
#         order = 1
#     elif letter == "M":
#         effective_year = year - 1
#         order = 2
#     else:
#         effective_year = year
#         order = 3

#     return effective_year, order


# def predict_offering(course_code, target_semester):
#     """
#     Reads Offering.xlsx and applies rule-based logic to determine
#     if `course_code` is likely to be offered in `target_semester`.
#     """
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     data_dir = os.path.join(current_dir, "..", "data", "course")
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

#     # Filter out columns that start with the target season AND have year > 20
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

#     fraction_offered = (
#         sum(offered_values) / len(offered_values) if offered_values else 0
#     )

#     threshold = 0.5
#     prediction = "YES" if fraction_offered >= threshold else "NO"

#     return {
#         "course_code": course_code,
#         "target_semester": target_semester,
#         "prediction": prediction,
#         "fraction_offered": fraction_offered
#     }


# def main():
#     """
#     Interactive mode for `predict_next_sem.py`.
#     Asks the user for target_semester and course_code,
#     then prints the prediction result.
#     """
#     target_semester = input(
#         "Enter the target future semester (e.g. S26): "
#     ).strip().upper()
#     course_input = input("Enter the Course Code to query: ").strip().upper()

#     result = predict_offering(course_input, target_semester)
#     print(result)


