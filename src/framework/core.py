import os
import glob
import logging
from typing import List, Dict, Any, Optional
from ollama import chat, embed
from src.utils.helpers import setup_logging, cosine_similarity

class BaseAgent:
    def __init__(self, model_name: str, config: Dict[str, Any], name: str, description: str, system_prompt: str = None):
        self.model_name = model_name
        self.config = config
        self.name = name
        self.description = description
        self.system_prompt = system_prompt or f"You are {self.name}, an expert in your domain."
        self.tools = []
        self.logger = logging.getLogger(self.name)

    def add_tool(self, tool: Dict[str, Any]):
        self.tools.append(tool)

    def call(self, prompt: str, messages: List[Dict[str, str]] = None) -> str:
        messages = messages or []
        full_messages = [{"role": "system", "content": self.system_prompt}] + messages + [{"role": "user", "content": prompt}]
        try:
            response = chat(model=self.model_name, messages=full_messages)
            content = response.get("message", {}).get("content", "").strip()
            return f"{self.name}: {content} End of {self.name} Response"
        except Exception as e:
            self.logger.error(f"Error in {self.name} call: {e}")
            return f"{self.name}: Error occurred: {str(e)} End of {self.name} Response"

    def get_embedding(self, text: str) -> List[float]:
        try:
            response = embed(model=self.config.get("embedding_model", "bge-m3:latest"), input=text)
            return response.get("embedding", [])
        except Exception as e:
            self.logger.error(f"Error generating embedding: {e}")
            return []

class RAG:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.cache = {}  # Cache for tools and agents
        self.logger = logging.getLogger("RAG")
        self.load_tools_and_agents()

    def load_tools_and_agents(self):
        # Load tools
        tool_dir = "src/tools"
        for tool_file in glob.glob(f"{tool_dir}/*.py"):
            if "__init__.py" in tool_file:
                continue
            module_name = os.path.basename(tool_file).replace(".py", "")
            module = __import__(f"src.tools.{module_name}", fromlist=["metadata", "execute"])
            self.cache[f"tool_{module_name}"] = {
                "name": module.metadata["name"],
                "description": module.metadata["description"],
                "embedding": self.get_embedding(module.metadata["description"]),
                "execute": module.execute
            }

        # Load agents
        agent_dir = "src/agents"
        for agent_file in glob.glob(f"{agent_dir}/*.py"):
            if "__init__.py" in agent_file:
                continue
            module_name = os.path.basename(agent_file).replace(".py", "")
            module = __import__(f"src.agents.{module_name}", fromlist=["Agent"])
            agent_instance = module.Agent(self.config)
            self.cache[f"agent_{module_name}"] = {
                "name": agent_instance.name,
                "description": agent_instance.description,
                "embedding": self.get_embedding(agent_instance.description),
                "instance": agent_instance
            }

    def get_embedding(self, text: str) -> List[float]:
        try:
            response = embed(model=self.config.get("embedding_model", "bge-m3:latest"), input=text)
            return response.get("embedding", [])
        except Exception as e:
            self.logger.error(f"Error in RAG embedding: {e}")
            return []

    def find_relevant_tools_and_agents(self, task: str, limit: int = 5) -> List[Dict[str, Any]]:
        task_embedding = self.get_embedding(task)
        if not task_embedding:
            return []

        ranked_items = []
        for item_name, item in self.cache.items():
            similarity = cosine_similarity(task_embedding, item["embedding"])
            ranked_items.append((similarity, item))

        ranked_items.sort(reverse=True)
        return [item for _, item in ranked_items[:limit]]