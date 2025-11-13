from functools import lru_cache
from typing import Dict, List, Optional

import pandas as pd

from api.v2.common import CSV_PATH


class V2Database:
    """Lightweight CSV-backed data access for v2 (no Flask/SQLAlchemy).

    Provides a pandas DataFrame and small helpers to map friendly column keys
    to dataset column names and compute numeric gross for sorting.
    """

    # Mapping to dataset column names (mirrors v1 mapping where possible)
    columns: Dict[str, str] = {
        "title": "Movie_Title",
        "year": "Year",
        "director": "Director",
        "actor": "Actors",
        "rating": "Rating",
        "runtime": '"Runtime(Mins)"',
        "censor": "Censor",
        "gross": "Total_Gross",
        "main_genre": "main_genre",
        "side_genre": "side_genre",
    }

    # Alias used in v1 for computed numeric gross (kept for compatibility)
    numeric_gross_title = "Gross(Million_Dollars)"

    def __init__(self, csv_path: Optional[str] = None):
        self.csv_path = csv_path or CSV_PATH
        self._df: Optional[pd.DataFrame] = None

    @property
    def dataframe(self) -> pd.DataFrame:
        if self._df is None:
            self._df = self._load_dataframe(self.csv_path)
        return self._df

    def reload(self):
        self._df = self._load_dataframe(self.csv_path)
        return self._df

    @staticmethod
    def _load_dataframe(csv_path: str) -> pd.DataFrame:
        df = pd.read_csv(csv_path)
        # Normalize column for runtime to match SQL quoted style used in v1 mapping
        if "Runtime(Mins)" in df.columns and '"Runtime(Mins)"' not in df.columns:
            df['"Runtime(Mins)"'] = df["Runtime(Mins)"]
        return df

    @staticmethod
    def parse_gross_to_float(value: str) -> float:
        """Convert strings like "$12.34M" to 12.34 (float)."""
        if not isinstance(value, str):
            try:
                return float(value)
            except Exception:
                return 0.0
        v = value.replace("$", "").replace("M", "").strip()
        try:
            return float(v)
        except Exception:
            return 0.0

    def add_numeric_gross(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        df = self.dataframe if df is None else df
        if self.numeric_gross_title not in df.columns:
            df = df.copy()
            df[self.numeric_gross_title] = df["Total_Gross"].map(
                self.parse_gross_to_float
            )
        return df

    def map_select_columns(self, select_clause: Optional[str]) -> Optional[List[str]]:
        if not select_clause:
            return None
        cols: List[str] = []
        for key in select_clause.split(","):
            key = key.strip()
            if key in self.columns:
                cols.append(self.columns[key])
        return cols or None


# Singleton-like accessor
@lru_cache(maxsize=1)
def get_db() -> V2Database:
    return V2Database()
