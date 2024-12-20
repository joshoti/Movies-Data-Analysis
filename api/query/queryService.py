from api.extensions.db import db_client


class QueryService:
    def get_data(self, query_params: dict) -> list:
        select_clause = query_params.get("select")
        where_clause = query_params.get("where")

        if not query_params:
            default_query = db_client.build_query(
                order_by=db_client.numeric_gross_title
            )
            return db_client.query_db(default_query)

        query = db_client.build_query(
            columns=select_clause,
            where_clause=where_clause,
        )

        return db_client.query_db(query)


query_service = QueryService()
