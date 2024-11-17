from typing import Union

from transformers import AutoModelForCausalLM, AutoTokenizer

from notebooks.google_tapas import google_tapas_client


class InferenceService:
    pipe = None

    def load_default_pipeline(self):
        self.pipe = google_tapas_client.get_pipeline()

    def use_hugging_face_pipeline(self, query: Union[str, list[str]]):
        """After generating answer from Tapas transformer, will pass result
        through text generation transformer to generate human-readable answers.
        """
        return self.pipe.use_qa_pipeline(query)

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
