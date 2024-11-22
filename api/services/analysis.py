from api.services.dbclient import db_client


class AnalysisService:
    def get_data(self, query_params: dict) -> list:
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
        """Movies By Genre Count"""

        chart_info = {"min_rating": 0, "max_rating": 10}
        result = []

        for genre in db_client.dataframe.main_genre.unique():
            genre_data = {"main_genre": genre}
            genre_data["count"] = len(
                db_client.dataframe[db_client.dataframe.main_genre == genre]
            )
            genre_data["rating"] = round(
                sum(
                    map(
                        float,
                        db_client.dataframe[
                            db_client.dataframe.main_genre == genre
                        ].Rating,
                    )
                )
                / genre_data["count"],
                2,
            )
            result.append(genre_data)

        chart_info["data"] = result
        return chart_info

    def get_example_two(self):
        pass

    def get_example_three(self):
        pass

    def get_example_four(self):
        pass

    def get_example_five(self):
        pass

    def get_example_six(self):
        [
            "UA", "U", "A", "Not Rated", "R", "18", "UA 16+", "PG", "PG-13",
            "U/A","7","16","(Banned)","13","12+","UA 13+","15+","12","All",
            "Unrated", "G", "UA 7+", "M/PG", "18+", "NC-17",
        ]
        """
        1. G, All, PG, M/PG
        2. 7, 15, 12, 13, PG-13, U, UA, U/A
        3 R, NC-17, 18, 18+, 16, UA 16+
        4. (Banned), Unrated, Not Rated
        """
        pass


analysis_service = AnalysisService()
