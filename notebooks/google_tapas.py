from transformers import AutoTokenizer, TapasForQuestionAnswering, pipeline

from api.services.dbclient import db_client
from interfaces import IQATransformerHelper


class GoogleTapasClient(IQATransformerHelper):
    """For Table Question Answering task"""

    model_name = "google/tapas-large-finetuned-wtq"
    pipe = None

    def get_pipeline(self):
        if self.pipe is None:
            # device = 0 or "mps" (GPU). Remove parameter, set to -1 or "cpu" to use CPU
            self.pipe = pipeline(model=self.model_name, device="mps")
        return self.pipe

    def use_qa_pipeline(self, query):
        return self.pipe(query=query, table=db_client.dataframe)["answer"]

    def use_qa_model(self):
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        model = TapasForQuestionAnswering.from_pretrained(self.model_name)

        return tokenizer, model


google_tapas_client = GoogleTapasClient()
