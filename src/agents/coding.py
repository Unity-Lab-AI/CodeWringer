from src.framework.core import BaseAgent

class CodingAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(
            model_name=config.get("coding_model", "qwen2.5-coder:14b-instruct-q4_K_M"),
            config=config,
            name="Code Agent",
            description="Specializes in code analysis, refactoring, and generation.",
            system_prompt="You are a coding expert. Provide detailed code analysis, refactoring suggestions, or generate code as requested."
        )

    def analyze_code(self, code: str) -> str:
        prompt = f"Analyze the following Python code for potential improvements and identify any bugs:\n\n{code}"
        return self.call(prompt)

    def refactor_code(self, code: str) -> str:
        prompt = f"Provide refactoring suggestions for the following Python code. Include variable renaming, improved readability, and potential bug fixes:\n\n{code}"
        return self.call(prompt)

    def generate_code(self, description: str) -> str:
        prompt = f"Generate Python code based on the following description:\n\n{description}"
        return self.call(prompt)