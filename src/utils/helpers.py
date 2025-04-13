import yaml
import logging
import os
from typing import Dict, Any, List
from pathlib import Path

def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from a YAML file."""
    try:
        with Path(config_path).open("r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return {}

def setup_logging(name: str, log_file: str, level: str = "INFO") -> logging.Logger:
    """Set up logging to file and console."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # File handler
    log_dir = Path(log_file).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    if not vec1 or not vec2 or len(vec1) != len(vec2):
        return 0.0
    try:
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5
        return dot_product / (norm1 * norm2) if norm1 and norm2 else 0.0
    except Exception as e:
        logging.getLogger("CosineSimilarity").error(f"Error calculating cosine similarity: {e}")
        return 0.0