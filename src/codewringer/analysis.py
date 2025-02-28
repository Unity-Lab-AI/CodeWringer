from .model import AIModel

def analyze_file(file_path: str) -> str:
    with open(file_path, 'r') as f:
        code = f.read()
    ai = AIModel()
    return ai.analyze_code(code)
