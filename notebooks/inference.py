from typing import List, Union

from transformers import AutoModelForCausalLM, AutoTokenizer

from interfaces import IQATransformerHelper
from notebooks.google_tapas import google_tapas_client
from notebooks.hugging_face_text_gen import hugging_face_text_gen_client  # noqa: F401


class InferenceService:
    client: IQATransformerHelper = None

    def load_default_qa_client(self):
        self.client = google_tapas_client
        self.client.get_pipeline()

    def use_hugging_face_pipeline(self, query: Union[str, List[str]]):
        """After generating answer from Table-Question-Answering
        transformer, will pass result through text generation transformer
        to generate human-readable answers.
        """

        if self.client is None:
            self.load_default_qa_client()

        raw_answer = self.client.use_qa_pipeline(query)
        # return hugging_face_text_gen_client.generate_human_readable_text(
        #     self.convert_answer_to_message(query, raw_answer)
        # )
        return raw_answer

    def convert_answer_to_message(self, query, answer):
        """Convert answer to message format that transformers are trained with"""

        content = f"Given a question '{query}', and answer '{answer}', generate a human-readable answer"
        return [{"role": "user", "content": content}]

    def use_model_pipeline(self, model_name="fine_tuned_model", use_tuned_model=True):
        if use_tuned_model:
            model = AutoModelForCausalLM.from_pretrained(model_name)
            tokenizer = AutoTokenizer.from_pretrained(model_name)
        else:
            tokenizer, model = google_tapas_client.use_qa_model()

        def ask_question(question):
            inputs = tokenizer.encode(question, return_tensors="pt")
            outputs = model.generate(inputs, max_length=50, num_return_sequences=1)
            answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
            return answer

        return ask_question


inference_service = InferenceService()
