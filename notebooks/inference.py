from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

from api.services.dbclient import db_client
from notebooks.google_tapex import google_tapas_client


class InferenceService:
    pipe = None

    def load_default_pipeline(self):
        self.pipe = pipeline(model=google_tapas_client.model_name)

    def use_hugging_face_pipeline(self, query):
        """After generating answer from Tapas transformer, will pass result
        through text generation transformer to generate human-readable answers.
        """
        return self.pipe(query=query, table=db_client.dataframe)["answer"]

    def qa_pipeline(self, model_name="fine_tuned_model"):
        model = AutoModelForCausalLM.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        def ask_question(question):
            inputs = tokenizer.encode(question, return_tensors="pt")
            outputs = model.generate(inputs, max_length=50, num_return_sequences=1)
            answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
            return answer

        return ask_question


inference_service = InferenceService()
