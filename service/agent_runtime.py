# ==========================================
# File: agent_runtime.py
# Handles execution of agent tasks based on 
# TaskDef_ID. This is the runtime engine for 
# Agent Processes.
#
# #ChatGPT (OpenAI, 2025) – Assisted in renaming 
# and refactoring to align with agent workflow 
# architecture and FYP guidelines.
# ==========================================

from task_logic.summarise import run_summarise
from task_logic.sentiment import run_sentiment


class AgentRuntime:
    """
    The runtime engine responsible for executing
    the agent's operations. In future this will support:
    - multi-stage flow
    - step-by-step task execution
    - guardrails & validation
    """

    @staticmethod
    def run_task(taskdef_id, file_path):
        """
        Routes to the correct task logic based on TaskDef_ID.
        """

        if taskdef_id == 1:
            return run_summarise(file_path)

        elif taskdef_id == 2:
            return run_sentiment(file_path)

        else:
            return "[Unsupported Task]"
