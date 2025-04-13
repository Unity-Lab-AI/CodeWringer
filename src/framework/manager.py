from typing import Dict, Any, List
from src.framework.core import BaseAgent, RAG
from src.utils.helpers import setup_logging

class ManagerAgent:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model_name = config.get("manager_model", "llama3.2")
        self.rag = RAG(config)
        self.agent = BaseAgent(
            model_name=self.model_name,
            config=config,
            name="Manager Agent",
            description="Orchestrates sub-agents and tools to complete tasks.",
            system_prompt="You are a manager agent, responsible for delegating tasks to sub-agents and tools."
        )
        self.logger = setup_logging("ManagerAgent", config.get("log_file", "logs/codewringer.log"))

    def run_task(self, task: str) -> str:
        self.logger.info(f"Received task: {task}")
        # Find relevant tools and agents using RAG
        relevant_items = self.rag.find_relevant_tools_and_agents(task, limit=self.config.get("tool_limit", 5))
        self.logger.info(f"Relevant items: {[item['name'] for item in relevant_items]}")

        # Prepare messages with available tools and agents
        tools_info = "\n".join([f"- Tool: {item['name']} - {item['description']}" for item in relevant_items if item['name'].startswith("tool_")])
        agents_info = "\n".join([f"- Agent: {item['name']} - {item['description']}" for item in relevant_items if item['name'].startswith("agent_")])
        prompt = f"Task: {task}\nAvailable Tools:\n{tools_info}\nAvailable Agents:\n{agents_info}\nHow would you proceed?"

        # Call the manager agent
        response = self.agent.call(prompt)
        self.logger.info(f"Manager response: {response}")

        # Parse response to delegate tasks
        for item in relevant_items:
            if item["name"] in response:
                if item["name"].startswith("tool_"):
                    # Execute tool
                    tool_name = item["name"].replace("tool_", "")
                    result = item["execute"](task)
                    self.logger.info(f"Tool {tool_name} result: {result}")
                    return result
                elif item["name"].startswith("agent_"):
                    # Delegate to sub-agent
                    sub_agent = item["instance"]
                    result = sub_agent.call(task)
                    self.logger.info(f"Agent {item['name']} result: {result}")
                    return result

        return response