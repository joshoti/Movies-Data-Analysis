from transformers import AutoTokenizer, TapasForQuestionAnswering, pipeline

from api.services.dbclient import db_client


class GoogleTapasClient:
    model_name = "google/tapas-large-finetuned-wtq"
    pipe = None

    def get_pipeline(self):
        if self.pipe is None:
            self.pipe = pipeline(model=google_tapas_client.model_name)
        return self.pipe

    def use_qa_pipeline(self, query):
        return self.pipe(query=query, table=db_client.dataframe)["answer"]

    def use_qa_model(self):
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        model = TapasForQuestionAnswering.from_pretrained(self.model_name)

        return tokenizer, model


google_tapas_client = GoogleTapasClient()
