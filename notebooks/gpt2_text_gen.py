from transformers import AutoModelForCausalLM, AutoTokenizer


class Gpt2TextGenerationClient:
    def __init__(self, model_name: str = "gpt2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def generate_human_readable_text(self, input_text: str):
        inputs = self.tokenizer(
            input_text, return_tensors="pt", padding=True, truncation=True
        )
        outputs = self.model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=50,
            num_return_sequences=1,
            pad_token_id=self.tokenizer.pad_token_id,
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
