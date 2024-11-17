from notebooks.inference import inference_service


class ProbingService:
    def answer_question(self, prompt: str):
        answer = inference_service.use_hugging_face_pipeline(prompt)
        return answer


probing_service = ProbingService()
