AutoModelForCausalLM = ...
AutoTokenizer = ...


class InferenceService:
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
