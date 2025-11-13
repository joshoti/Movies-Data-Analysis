from typing import Dict, List

import pandas as pd

from .db_client import get_db


class QueryService:
    def __init__(self):
        self.db = get_db()

    def get_data(self, query_params: Dict[str, str]) -> List[Dict]:
        select_clause = query_params.get("select") if query_params else None
        where_clause = query_params.get("where") if query_params else None

        df = self.db.dataframe

        # Default behavior: order by numeric gross desc and limit 30
        if not query_params:
            df_num = self.db.add_numeric_gross(df)
            df_sorted = df_num.sort_values(self.db.numeric_gross_title, ascending=False)
            return df_sorted.head(30).to_dict(orient="records")

        # Apply where filters
        df_filtered = self._apply_where(df, where_clause) if where_clause else df

        # Column selection (map friendly keys to dataset columns)
        cols = self.db.map_select_columns(select_clause)
        if cols:
            df_selected = df_filtered[cols]
        else:
            df_selected = df_filtered

        # Limit default 30 to mirror v1
        return df_selected.head(30).to_dict(orient="records")

    def _apply_where(self, df: pd.DataFrame, query_string: str) -> pd.DataFrame:
        """Replicates v1 build_where_clause logic for a pandas DataFrame.

        where format: "AND-column-operator-value,OR-column-operator-value,..."
        Supported operators: =, LIKE (substring, case-insensitive), >, >=, <, <=
        """

        if not query_string:
            return df

        def one_predicate(
            sub_df: pd.DataFrame, column_key: str, operator: str, value: str
        ) -> pd.Series:
            col_name = self.db.columns.get(column_key)
            if not col_name or col_name not in sub_df.columns:
                # Unknown column -> all False mask
                return pd.Series([False] * len(sub_df), index=sub_df.index)

            series = sub_df[col_name]

            # Special handling: Total_Gross comparisons -> convert to float
            if column_key == "gross":
                series = series.map(self.db.parse_gross_to_float)
                try:
                    value_num = float(value.replace("$", "").replace("M", ""))
                except Exception:
                    value_num = 0.0
                if operator == ">":
                    return series > value_num
                if operator == ">=":
                    return series >= value_num
                if operator == "<":
                    return series < value_num
                if operator == "<=":
                    return series <= value_num
                if operator in ("=", "=="):
                    return series == value_num

            # Numeric comparisons for year, rating, runtime
            if column_key in {"year", "rating", "runtime"}:

                def to_float(x):
                    try:
                        return float(x)
                    except Exception:
                        return float("nan")

                series_num = series.map(to_float)
                try:
                    value_num = float(value)
                except Exception:
                    return pd.Series([False] * len(sub_df), index=sub_df.index)

                if operator == ">":
                    return series_num > value_num
                if operator == ">=":
                    return series_num >= value_num
                if operator == "<":
                    return series_num < value_num
                if operator == "<=":
                    return series_num <= value_num
                if operator in ("=", "=="):
                    return series_num == value_num

            # Default string comparisons
            series_str = series.astype(str)
            if operator.upper() == "LIKE":
                # value expected without % in query; v1 wraps with % ... %
                needle = str(value).lower()
                return series_str.str.lower().str.contains(needle, na=False)
            if operator in ("=", "=="):
                return series_str == str(value)

            # Fallback: no match
            return pd.Series([False] * len(sub_df), index=sub_df.index)

        mask = None
        for stmt in query_string.split(","):
            logic, column, operator, value = [
                part.strip() for part in stmt.split("-", 3)
            ]
            pred = one_predicate(df, column, operator, value)
            if mask is None:
                mask = pred
            else:
                if logic.upper() == "AND":
                    mask = mask & pred
                else:
                    mask = mask | pred

        if mask is None:
            return df
        return df[mask]


query_service = QueryService()
