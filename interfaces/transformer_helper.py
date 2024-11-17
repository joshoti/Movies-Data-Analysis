from abc import ABC
from typing import List, Union


class TransformerHelperInterface(ABC):
    """For Table Question Answering task"""

    def get_pipeline(self):
        pass

    def use_qa_pipeline(self, query: Union[str, List[str]]):
        pass

    def use_qa_model(self):
        pass
