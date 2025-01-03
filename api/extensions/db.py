from threading import Thread
from typing import Union

import pandas as pd
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


class DatabaseClient:
    table_name = "Movies"
    numeric_gross_title = "'Gross(Million_Dollars)'"
    _dataframe: pd.DataFrame = None

    columns = {
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
        # "gross": numeric_gross_title,
    }

    @property
    def dataframe(self):
        if self._dataframe is None:
            with current_app.app_context():
                db_client.init_db(csv_path)
                Thread(target=db_client.load_dataframe).run()
        return self._dataframe

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

        if self._dataframe is not None:
            return

        self._dataframe = pd.read_sql_query(
            f'SELECT \
                Movie_Title, CAST(Year AS VARCHAR) AS Year, Director, \
                Actors, CAST(Rating AS VARCHAR) AS Rating, \
                CAST("Runtime(Mins)" AS VARCHAR) AS Runtime, \
                Censor, Total_Gross, main_genre, side_genre \
            FROM {self.table_name}',
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
        columns: str = None,
        include_numerical_gross: bool = False,
        table_name: str = "",
        where_clause: str = "",
        order_by: str = "",
        limit: int = 30,
    ):
        columns = "*" if not columns else self.build_select(columns)
        columns += self.gross_function() if include_numerical_gross else ""

        table_name = self.table_name

        where_clause = db_client.build_where_clause(where_clause)

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

    def build_select(self, columns: str) -> str:
        select_predicate = []
        for column in columns.split(","):
            select_predicate.append(self.columns[column])
        return ",".join(select_predicate)

    def build_where_clause(self, query_string: str) -> str:
        if not query_string:
            return ""

        where_clause = ""
        for stmt in query_string.split(","):
            logic, column, operator, value = stmt.split("-")

            if operator == "LIKE":
                value = "%" + value + "%"

            where_clause += f"{logic} {self.columns[column]} {operator} '{value}' "

        return where_clause.removeprefix("AND ").removeprefix("OR ")

    def filter_columns(self, query: Union[str, list[str]] = None):
        """Filter columns based on query"""

        if query is None or self._dataframe is None:
            return self.dataframe

        keyword_to_column_mapping = {
            "title": "Movie_Title",
            "when": "Year",
            "year": "Year",
            "old": "Year",
            "director": "Director",
            "directors": "Director",
            "producer": "Director",
            "producers": "Director",
            "actor": "Actors",
            "actors": "Actors",
            "star": "Actors",
            "stars": "Actors",
            "movie star": "Actors",
            "movie stars": "Actors",
            "rating": "Rating",
            "well": "Rating",
            "perform": "Rating",
            "runtime": '"Runtime(Mins)"',
            "time": '"Runtime(Mins)"',
            "long": '"Runtime(Mins)"',
            "length": '"Runtime(Mins)"',
            "age": "Censor",
            "young": "Censor",
            "censor": "Censor",
            "viewer": "Censor",
            "viewers": "Censor",
            "viewership": "Censor",
            "earn": "Total_Gross",
            "earned": "Total_Gross",
            "much": "Total_Gross",
            "money": "Total_Gross",
            "revenue": "Total_Gross",
            "gross": "Total_Gross",
            "genre": "main_genre",
            "kind": "main_genre",
        }

        columns_to_keep = set(["Movie_Title"])
        if isinstance(query, list):
            query = " ".join(query)

        for word in query.split(" "):
            word = word.strip().lower()
            if word in keyword_to_column_mapping:
                columns_to_keep.add(keyword_to_column_mapping[word])
        return self.dataframe.filter(items=columns_to_keep)


db_client = DatabaseClient()
csv_path = "./data/external/MoviesDataset.csv"
