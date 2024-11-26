from collections import defaultdict
from typing import Union

from api.services.dbclient import db_client


class AnalysisService:
    def get_data(self, query_params: dict) -> Union[list, dict]:
        where_clause = db_client.build_where_clause(query_params["query"])

        if not query_params:
            default_query = db_client.build_query(
                order_by=db_client.numeric_gross_title
            )
            return db_client.query_db(default_query)

        query = db_client.build_query(
            where_clause=where_clause, order_by=db_client.numeric_gross_title
        )

        return db_client.query_db(query)

    def get_sample_data(self, example_id: str) -> dict:
        sample_mapping = {
            "sample-1": self.get_example_one,
            "sample-2": self.get_example_two,
            "sample-3": self.get_example_three,
            "sample-4": self.get_example_four,
            "sample-5": self.get_example_five,
            "sample-6": self.get_example_six,
        }
        return sample_mapping[example_id]()

    def get_example_one(self):
        """Average Rating By Movies Count Vs Genre"""

        chart_info = {"min_rating": 6, "max_rating": 7.5}
        genre_data_accumulator = []
        genre_counter = defaultdict(int)
        genre_rating = defaultdict(float)

        for index in range(len(db_client.dataframe)):
            row = db_client.dataframe.iloc[index]

            genre, rating = row.main_genre, float(row.Rating)

            genre_counter[genre] += 1
            genre_rating[genre] += rating

        for genre, count in genre_counter.items():
            rating = genre_rating[genre]

            genre_data = {"main_genre": genre}
            genre_data["rating"] = round(rating / count, 1)
            genre_data["count"] = count

            genre_data_accumulator.append(genre_data)

        chart_info["data"] = genre_data_accumulator
        return chart_info

    def get_example_two(self) -> list:
        """Rating by Runtime"""

        chart_info = []
        runtime_rating = defaultdict(float)
        runtime_counter = defaultdict(int)

        for index in range(len(db_client.dataframe)):
            row = db_client.dataframe.iloc[index]
            rating, runtime = float(row.Rating), float(row.Runtime)

            runtime = (runtime // 10) * 10
            runtime_counter[runtime] += 1
            runtime_rating[runtime] += rating

        for runtime in sorted(runtime_counter):
            count = runtime_counter[runtime]

            runtime_data = {}
            runtime_data["runtime"] = runtime
            runtime_data["rating"] = round(runtime_rating[runtime] / count, 1)

            chart_info.append(runtime_data)

        return chart_info

    def get_example_three(self) -> dict:
        """Total Gross By Movies Count Vs Year"""

        chart_info = {"min_gross": 0, "max_gross": 98_000}
        result = []

        year_gross = defaultdict(float)
        year_counter = defaultdict(int)

        for index in range(len(db_client.dataframe)):
            row = db_client.dataframe.iloc[index]
            gross, year = row.Total_Gross, int(row.Year)

            # preprocessing to convert to decimal
            gross = float(gross.removeprefix("$").removesuffix("M"))
            year = (year // 10) * 10

            year_counter[year] += 1
            year_gross[year] += gross

        for year in sorted(year_counter):
            count = year_counter[year]

            year_data = {}
            year_data["year"] = year
            year_data["count"] = count
            year_data["total_gross"] = round(year_gross[year], 2)

            result.append(year_data)

        chart_info["data"] = result
        return chart_info

    def get_example_four(self):
        """Gross By Runtime Vs Genre"""

        chart_info = []
        genre_runtime = defaultdict(int)
        genre_gross = defaultdict(float)

        for index in range(len(db_client.dataframe)):
            row = db_client.dataframe.iloc[index]

            genre, runtime = row.main_genre, int(row.Runtime)

            # preprocessing to convert to decimal
            gross = float(row.Total_Gross.removeprefix("$").removesuffix("M"))

            genre_runtime[genre] += runtime
            genre_gross[genre] += gross

        for genre, runtime in genre_runtime.items():
            gross = genre_gross[genre]

            genre_data = {"main_genre": genre}
            genre_data["total_gross"] = round(gross, 2)  # Floating-point arithmetic
            genre_data["runtime"] = runtime

            chart_info.append(genre_data)

        return chart_info

    def get_example_five(self):
        pass

    def get_example_six(self):
        [
            "UA",
            "U",
            "A",
            "Not Rated",
            "R",
            "18",
            "UA 16+",
            "PG",
            "PG-13",
            "U/A",
            "7",
            "16",
            "(Banned)",
            "13",
            "12+",
            "UA 13+",
            "15+",
            "12",
            "All",
            "Unrated",
            "G",
            "UA 7+",
            "M/PG",
            "18+",
            "NC-17",
        ]
        """
        1. G, All, PG, M/PG
        2. 7, 15, 12, 13, PG-13, U, UA, U/A
        3 R, NC-17, 18, 18+, 16, UA 16+
        4. (Banned), Unrated, Not Rated
        """
        pass


analysis_service = AnalysisService()
