"""
This module provides a base class for data extraction functionalities.
It includes methods for saving data to Excel and loading JSON files.
"""

import json
import logging
from typing import Any, List, Union
import pandas as pd

class DataExtractor:
    """
    Base class for data extraction functionalities.
    Provides common methods for saving data to Excel and loading JSON files.
    """
    def __init__(self) -> None:
        logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    @staticmethod
    def save_to_excel(data: Union[pd.DataFrame, List[dict]], output_path: str) -> None:
        """
        Saves the provided data to an Excel file.
        Catches only the exceptions expected during file writing and DataFrame conversion.
        """
        try:
            if data is None or (isinstance(data, pd.DataFrame) and
                data.empty) or (not isinstance(data, pd.DataFrame) and not data):
                logging.warning("No data to save for %s", output_path)
                return

            df = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)
            df.to_excel(output_path, index=False)
            logging.info("Data successfully saved to %s", output_path)
        except (OSError, ValueError) as error:
            logging.error("Error saving to %s: %s", output_path, error)
