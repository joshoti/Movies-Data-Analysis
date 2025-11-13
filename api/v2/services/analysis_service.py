from collections import defaultdict

from .db_client import get_db


class AnalysisService:
    def __init__(self):
        self.db = get_db()

    def get_sample_data(self, example_id: str) -> dict | list:
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

        chart_info: dict = {"min_rating": 6, "max_rating": 7.5}
        genre_data_accumulator = []
        genre_counter = defaultdict(int)
        genre_rating = defaultdict(float)

        df = self.db.dataframe
        for _, row in df.iterrows():
            genre = row["main_genre"]
            try:
                rating = float(row["Rating"])
            except Exception:
                continue

            genre_counter[genre] += 1
            genre_rating[genre] += rating

        for genre, count in genre_counter.items():
            total_rating = genre_rating[genre]

            genre_data = {"main_genre": genre}
            genre_data["rating"] = round(total_rating / count, 1)
            genre_data["count"] = count

            genre_data_accumulator.append(genre_data)

        chart_info["data"] = genre_data_accumulator
        return chart_info

    def get_example_two(self) -> list:
        """Rating by Runtime"""

        chart_info = []
        runtime_rating = defaultdict(float)
        runtime_counter = defaultdict(int)

        df = self.db.dataframe
        runtime_col = (
            '"Runtime(Mins)"' if '"Runtime(Mins)"' in df.columns else "Runtime(Mins)"
        )

        for _, row in df.iterrows():
            try:
                rating = float(row["Rating"])
                runtime = float(row[runtime_col])
            except Exception:
                continue

            runtime_bucket = (runtime // 10) * 10
            runtime_counter[runtime_bucket] += 1
            runtime_rating[runtime_bucket] += rating

        for runtime in sorted(runtime_counter):
            count = runtime_counter[runtime]
            runtime_data = {
                "runtime": runtime,
                "rating": round(runtime_rating[runtime] / count, 1),
            }
            chart_info.append(runtime_data)

        return chart_info

    def get_example_three(self) -> dict:
        """Total Gross By Movies Count Vs Year"""

        chart_info = {"min_gross": 0, "max_gross": 98000}
        result = []

        df = self.db.dataframe
        year_gross = defaultdict(float)
        year_counter = defaultdict(int)

        for _, row in df.iterrows():
            try:
                year = int(row["Year"])
            except Exception:
                continue

            gross = self.db.parse_gross_to_float(row["Total_Gross"])  # in millions
            year_bucket = (year // 10) * 10

            year_counter[year_bucket] += 1
            year_gross[year_bucket] += gross

        for year in sorted(year_counter):
            count = year_counter[year]
            year_data = {
                "year": year,
                "count": count,
                "total_gross": round(year_gross[year], 2),
            }
            result.append(year_data)

        chart_info["data"] = result
        return chart_info

    def get_example_four(self):
        """Gross By Runtime Vs Genre"""

        chart_info = []
        genre_runtime = defaultdict(int)
        genre_gross = defaultdict(float)

        df = self.db.dataframe
        runtime_col = (
            '"Runtime(Mins)"' if '"Runtime(Mins)"' in df.columns else "Runtime(Mins)"
        )

        for _, row in df.iterrows():
            genre = row["main_genre"]
            try:
                runtime = int(float(row[runtime_col]))
            except Exception:
                continue

            gross = self.db.parse_gross_to_float(row["Total_Gross"])  # in millions

            genre_runtime[genre] += runtime
            genre_gross[genre] += gross

        for genre, runtime in genre_runtime.items():
            gross = genre_gross[genre]

            genre_data = {"main_genre": genre}
            genre_data["total_gross"] = round(gross, 2)
            genre_data["runtime"] = runtime

            chart_info.append(genre_data)

        return chart_info

    def get_example_five(self):
        """Censor Rating Vs Year"""

        chart_info = []
        censor_year_count = defaultdict(dict)

        df = self.db.dataframe

        for _, row in df.iterrows():
            try:
                year = int(row["Year"])
            except Exception:
                continue
            censor = row["Censor"]

            year_bucket = (year // 10) * 10
            censor_key = self.censorMapping(censor)

            # dict in dict e.g. {1930: {'pg_movies': 6, 'unrated_movies': 17, 'g_movies': 1}}
            censor_year_count[year_bucket][censor_key] = 1 + censor_year_count[
                year_bucket
            ].get(censor_key, 0)

        for year in sorted(censor_year_count):
            censor_count = censor_year_count[year]
            censor_year_data: dict = dict(censor_count)
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
