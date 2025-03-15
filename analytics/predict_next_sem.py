import os
import pandas as pd
import numpy as np


def semester_sort_key(sem):
    """
    Sort a semester code based on an academic cycle:
      - For Fall (F): effective_year = int(year), order = 0.
      - For Spring (S) and Summer (M): effective_year = int(year) - 1,
        order = 1 for Spring, 2 for Summer.
    For example:
      F20 -> (20, 0)
      S21 -> (20, 1)
      M21 -> (20, 2)
      F21 -> (21, 0)
    """
    letter = sem[0].upper()
    try:
        year = int(sem[1:])
    except Exception:
        year = 0

    if letter == "F":
        effective_year = year
        order = 0
    elif letter == "S":
        effective_year = year - 1
        order = 1
    elif letter == "M":
        effective_year = year - 1
        order = 2
    else:
        effective_year = year
        order = 3

    return effective_year, order


def main():
    # Construct the path to the 'data/course' folder (assuming this script is in a subfolder)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "..", "data", "course")
    offering_file = os.path.join(data_dir, "Offering.xlsx")

    df = pd.read_excel(offering_file, engine="openpyxl")
    df.columns = df.columns.str.strip()
    df["Offered"] = 1

    grouped = df.groupby(["course_code", "semester"])["Offered"].max().reset_index()
    unique_semesters = grouped["semester"].unique()
    sorted_semesters = sorted(unique_semesters, key=semester_sort_key)
    print("Sorted semesters:", sorted_semesters)

    wide_data = grouped.pivot(index="course_code", columns="semester", values="Offered")
    wide_data = wide_data.reindex(columns=sorted_semesters, fill_value=0)
    wide_data = wide_data.reset_index()
    wide_data.columns.name = None
    wide_data = wide_data.fillna(0)

    #####################################
    #      RULE-BASED PREDICTION STEP   #
    #####################################

    # Ask the user for a target future semester, e.g., "S26"
    target_semester = input(
        "\nEnter the target future semester (e.g., S26): "
    ).strip().upper()
    target_season = target_semester[0]  # "S", "F", or "M"

    # Ask the user for a course code to query
    course_input = input("Enter the Course Code to query: ").strip().upper()

    # Locate the row for that course
    course_row = wide_data[wide_data["course_code"] == course_input]

    if course_row.empty:
        print(f"Course {course_input} not found in the data.")
    else:
        # Filter out columns that start with the target season AND have a year > 20
        season_cols = [
            col
            for col in sorted_semesters
            if col.startswith(target_season) and int(col[1:]) > 20
        ]

        # Gather the offering values for these columns
        offered_values = []
        for col in season_cols:
            if col in course_row.columns:
                offered_values.append(int(course_row[col].iloc[0]))
            else:
                offered_values.append(0)

        # Calculate the fraction of times the course was offered
        fraction_offered = sum(offered_values) / len(offered_values) if offered_values else 0

        print(
            f"\nFor course {course_input} in past {target_season} semesters after year 20:"
        )
        print(
            f"Offered in {sum(offered_values)} out of {len(offered_values)} semesters "
            f"(fraction = {fraction_offered:.2f})"
        )

        # Simple threshold-based prediction
        threshold = 0.5
        prediction = "YES" if fraction_offered >= threshold else "NO"
        print(
            f"\nRule-based prediction: Will course {course_input} be offered in "
            f"{target_semester}? {prediction}"
        )


if __name__ == "__main__":
    main()
