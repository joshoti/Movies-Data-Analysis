from api.v1.config import Config


class TestConfig(Config):
    DEBUG = True
    TESTING = True


chat_prompt_1 = "what genre of movie should I make to earn more than $300M?"
chat_prompt_2 = "What movies earned more than $300M?"
