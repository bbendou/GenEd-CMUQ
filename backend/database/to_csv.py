"""
This script is used to export the database tables to CSV files. for easy viewing and editing.
"""
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Load database URL (Default: SQLite)
DATABASE_URL = "sqlite:///backend/database/gened_db.sqlite"

# Create the engine
engine = create_engine(DATABASE_URL)

# Define the tables you want to export
tables = [
    "department",
    "course",
    "offering",
    "requirement",
    "audit",
    "countsfor",
    "prereqs",
    "course_instructor",
    "enrollment"
]

# Create a directory to save the CSV files
OUTPUT_DIR = "data/csv_exports"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Export each table to a CSV file
for table in tables:
    try:
        # Read the table into a DataFrame
        df = pd.read_sql_table(table, con=engine)

        # Define the output file path
        output_file = os.path.join(OUTPUT_DIR, f"{table}.csv")

        # Write the DataFrame to a CSV file
        df.to_csv(output_file, index=False)
        print(f"Exported {table} to {output_file}")

    except SQLAlchemyError as e:
        print(f"Database error while exporting {table}: {e}")
    except FileNotFoundError as e:
        print(f"File not found error while exporting {table}: {e}")
    except pd.errors.EmptyDataError as e:
        print(f"Empty data error while exporting {table}: {e}")
    except Exception as e: # pylint: disable=broad-exception-caught
        print(f"Unexpected error while exporting {table}: {e}")
