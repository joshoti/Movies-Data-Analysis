from api.config import Config


class TestConfig(Config):
    DEBUG = True
    TESTING = True


predict_prompt = "what genre of movie should I make to earn more than $300M?"
probe_prompt = "What movies earned more than $300M?"
