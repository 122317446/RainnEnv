# ==========================================
# File: agent_runtime.py
# Created in iteration: 2
# Author: Karl Concha
#
# ChatGPT (OpenAI, 2025) – Assisted in renaming and
# refactoring the runtime routing structure to align
# with the agent workflow design and FYP Bible
# requirements on code clarity and maintainability.
# Conversation Topic: "Iteration 2 – Agent runtime
# routing and operation dispatch refinement."
# Date of assistance: November 2025
#
# References:
# - None (runtime logic developed manually; only
#   ChatGPT assistance noted above)
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
