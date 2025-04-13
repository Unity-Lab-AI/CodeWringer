from src.framework.core import BaseAgent

class ResearchAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(
            model_name=config.get("research_model", "llama3.2"),
            config=config,
            name="Research Agent",
            description="Generates topics and answers questions using web-augmented data.",
            system_prompt="You are a research assistant. Generate topics or answer questions using web data when available."
        )

    def generate_topic(self, subject: str, previous_topics: set) -> str:
        prompt = f"Generate a unique topic for the subject '{subject}'. Avoid these topics: {', '.join(previous_topics)}."
        return self.call(prompt)

    def answer_question(self, question: str, web_context: str = None) -> str:
        if web_context:
            prompt = f"Answer the following question using the provided web context:\nQuestion: {question}\nWeb Context:\n{web_context}"
        else:
            prompt = f"Answer the following question:\n{question}"
        return self.call(prompt)