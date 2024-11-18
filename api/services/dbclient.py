import pandas as pd
from sqlalchemy import text

from ..extensions.db import db


class DatabaseClient:
    table_name = "Movies"
    numeric_gross_title = "'Gross(Million_Dollars)'"
    dataframe = None

    columns = {
        "title": "Movie_Title",
        "year": "Year",
        "director": "Director",
        "actor": "Actors",
        "rating": "Rating",
        "runtime": "Runtime(Mins)",
        "censor": "Censor",
        # "gross": "Total_Gross",
        "main_genre": "main_genre",
        "side_genre": "side_genre",
        "gross": numeric_gross_title,
    }

    operators = {
        "eq": "=",
        "lt": "<",
        "le": "<=",
        "gt": ">",
        "ge": ">=",
        "not": "NOT",
        "like": "LIKE",
    }

    def init_db(self, file_path: str):
        self.load_db_in_disk(file_path)
        self.handle_missing_records()

    def load_db_in_disk(self, file_path: str):
        try:
            result = db.session.execute(
                text(
                    f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}';"
                )
            ).scalar_one_or_none()

            if not result:
                database = pd.read_csv(file_path)
                database.to_sql(
                    self.table_name,
                    db.session.connection(),
                    index=False,
                    if_exists="replace",
                )
                db.session.commit()

        except Exception:
            print("Error while initializing database")

    def handle_missing_records(self):
        db.session.execute(
            text(
                f'UPDATE {self.table_name} \
                SET Total_Gross = "$0.00M" \
                WHERE Total_Gross = "Gross Unkown"'
            )
        )
        db.session.commit()

    def load_dataframe(self):
        """Loading all numerical columns as VARCHAR"""

        if self.dataframe:
            return

        self.dataframe = pd.read_sql_query(
            f"SELECT \
                Movie_Title, CAST(Year AS VARCHAR) AS Year, Director, \
                Actors, CAST(Rating AS VARCHAR) AS Rating, \
                CAST('Runtime(Mins)' AS VARCHAR) AS 'Runtime(Mins)', \
                Censor, Total_Gross, main_genre, side_genre \
            FROM {self.table_name}",
            db.session.connection(),
        )

    def gross_function(self):
        """The Total_Gross column is in VARCHAR format. This function
        converts the column to numerical equivalent for comparison
        """

        return (
            ", CAST("
            "REPLACE(REPLACE(Total_Gross, '$', ''), 'M', '') AS DECIMAL(10, 2)"
            f") AS {self.numeric_gross_title}"
        )

    def build_query(
        self,
        columns: list[str] = None,
        include_numerical_gross: bool = True,
        table_name: str = "",
        where_clause: str = "",
        order_by: str = "",
        limit: int = 10,
    ):
        columns = "*" if not columns else ",".join(columns)
        columns += self.gross_function() if include_numerical_gross else ""

        table_name = self.table_name

        query = f"SELECT {columns} "
        query += f"FROM {table_name} "
        query += f"WHERE {where_clause} " if where_clause else ""
        query += f"ORDER BY {order_by} DESC " if order_by else ""
        query += f"LIMIT {limit};"
        return query

    def query_db(self, sql_query) -> list[dict]:
        result = [
            dict(record)
            for record in db.session.execute(text(sql_query)).mappings().all()
        ]
        return result

    def build_where_clause(self, query_params: str) -> str:
        where_clause = []
        for stmt in query_params.split(","):
            column, operator, value = stmt.split("-")

            if operator == "like":
                value = "%" + value + "%"

            where_clause.append(
                f"{self.columns[column]} {self.operators[operator]} '{value}'"
            )

        return " AND ".join(where_clause)


db_client = DatabaseClient()
