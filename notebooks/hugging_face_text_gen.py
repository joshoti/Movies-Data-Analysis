from typing import Dict, List

from transformers import pipeline

from api.v1.interfaces import ITextGenTransformerHelper


class HuggingFaceTextGenerationClient(ITextGenTransformerHelper):
    model_name = "HuggingFaceTB/SmolLM2-1.7B-Instruct"

    def generate_human_readable_text(self, messages: List[Dict[str, str]]):
        """Check super class for sample message format"""

        pipe = pipeline("text-generation", model=self.model_name)
        return pipe(messages, max_new_tokens=128)


hugging_face_text_gen_client = HuggingFaceTextGenerationClient()
