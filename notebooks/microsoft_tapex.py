from transformers import BartForConditionalGeneration, TapexTokenizer, pipeline

from api.extensions.db import db_client
from interfaces import IQATransformerHelper


class MicrosoftTapexClient(IQATransformerHelper):
    """For Table Question Answering task"""

    model_name = "microsoft/tapex-large-finetuned-wtq"
    pipe = None

    def get_pipeline(self):
        if self.pipe is None:
            self.pipe = pipeline(model=self.model_name)
        return self.pipe

    def use_qa_pipeline(self, query):
        return self.pipe(query=query, table=db_client.filter_columns(query))

    def use_qa_model(self):
        tokenizer = TapexTokenizer.from_pretrained(self.model_name)
        model = BartForConditionalGeneration.from_pretrained(self.model_name)

        return tokenizer, model
