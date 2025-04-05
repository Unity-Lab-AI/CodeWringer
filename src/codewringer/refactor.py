from .model import AIModel

def refactor_file(file_path: str) -> str:
    with open(file_path, 'r') as f:
        code = f.read()
    ai = AIModel()
    return ai.refactor_code(code)
