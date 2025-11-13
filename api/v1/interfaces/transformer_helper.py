from abc import ABC
from typing import Dict, List, Union


class IQATransformerHelper(ABC):
    """For Table Question Answering task"""

    def get_pipeline(self):
        pass

    def use_qa_pipeline(self, query: Union[str, List[str]]) -> str:
        pass

    def use_qa_model(self):
        pass


class ITextGenTransformerHelper(ABC):
    """For Text Generation task"""

    def get_pipeline(self):
        pass

    def generate_human_readable_text(self, messages: List[Dict[str, str]]):
        """
        sample messages
        >>> [{
            "role": "user",
            "content": "Sing me a song",
        },]
        """
        pass

    def use_text_gen_model(self):
        pass
