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
        """Censor Rating Vs Year"""

        chart_info = []
        censor_year_count = defaultdict(dict)

        for index in range(len(db_client.dataframe)):
            row = db_client.dataframe.iloc[index]

            year, censor = int(row.Year), row.Censor

            year = (year // 10) * 10
            censor = self.censorMapping(censor)

            # dict in dict e.g. {1930: {'pg_movies': 6, 'unrated_movies': 17, 'g_movies': 1}}
            censor_year_count[year][censor] = 1 + censor_year_count[year].get(censor, 0)

        for year in sorted(censor_year_count):
            censor_count = censor_year_count[year]

            censor_year_data: dict = censor_count
            censor_year_data["year"] = year

            chart_info.append(censor_year_data)

        return chart_info

    @staticmethod
    def censorMapping(censor_rating: str):
        censor_map = {
            "G": "g_movies",  # G Movies
            "All": "g_movies",
            "PG": "pg_movies",  # PG Movies
            "PG-13": "pg_movies",
            "M/PG": "pg_movies",
            "U/A": "pg_movies",
            "UA": "pg_movies",
            "U": "pg_movies",
            "A": "pg_movies",
            "7": "pg_movies",
            "13": "pg_movies",
            "12+": "pg_movies",
            "UA 13+": "pg_movies",
            "15+": "pg_movies",
            "12": "pg_movies",
            "UA 7+": "pg_movies",
            "R": "r_movies",  # R Movies
            "18": "r_movies",
            "UA 16+": "r_movies",
            "16": "r_movies",
            "NC-17": "r_movies",
            "18+": "r_movies",
            "Unrated": "unrated_movies",  # Unrated Movies
            "(Banned)": "unrated_movies",
            "Not Rated": "unrated_movies",
        }
        return censor_map.get(censor_rating, "unrated_movies")


analysis_service = AnalysisService()
