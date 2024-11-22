from api.services.dbclient import db_client


class QueryService:
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


analysis_service = QueryService()
