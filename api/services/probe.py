from ..services.inference import inference_service


class ProbingService:
    def answer_question(self, prompt: str):
        probe = inference_service.qa_pipeline()
        return probe(prompt)


probing_service = ProbingService()
