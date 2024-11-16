from ..services.inference import inference_service


class PredictionService:
    def answer_question(self, prompt: str):
        predict = inference_service.qa_pipeline()
        return predict(prompt)


prediction_service = PredictionService()
