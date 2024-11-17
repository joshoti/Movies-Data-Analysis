from transformers import BartForConditionalGeneration, TapexTokenizer, pipeline

from api.services.dbclient import db_client

from ..interfaces import TransformerHelperInterface


class MicrosoftTapexClient(TransformerHelperInterface):
    """For Table Question Answering task"""

    model_name = "microsoft/tapex-large-finetuned-wtq"

    def get_pipeline(self):
        if self.pipe is None:
            self.pipe = pipeline(model=self.model_name)
        return self.pipe

    def use_qa_pipeline(self, query):
        return self.pipe(query=query, table=db_client.dataframe)

    def use_qa_model(self):
        tokenizer = TapexTokenizer.from_pretrained(self.model_name)
        model = BartForConditionalGeneration.from_pretrained(self.model_name)

        return tokenizer, model
