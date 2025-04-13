from ollama import embed
import logging

metadata = {
    "name": "embed",
    "description": "Generates embeddings for text using the configured embedding model."
}

def execute(task: str) -> str:
    logger = logging.getLogger("EmbedTool")
    try:
        response = embed(model="bge-m3:latest", input=task)
        embedding = response.get("embedding", [])
        logger.info(f"Embedding generated for text: {task[:50]}...")
        return str(embedding)
    except Exception as e:
        logger.error(f"Embedding failed for '{task[:50]}...': {e}")
        return f"Error: {str(e)}"