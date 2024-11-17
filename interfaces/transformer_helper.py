from abc import ABC

class TransformerHelperInterface(ABC):
    """For Table Question Answering task"""

    def get_pipeline(self):
        pass

    def use_qa_pipeline(self, query: str):
        pass

    def use_qa_model(self):
        pass