# ==========================================
# Handles routing to the correct task logic
# based on TaskDef_ID.
# ==========================================

from task_logic.summarise import run_summarise
from task_logic.sentiment import run_sentiment

class AgentProcessing:

    @staticmethod
    def run_task(taskdef_id, file_path):
        """
        Receives TaskDef_ID + path to file to process.
        Sends file to correct task logic module.
        """

        if taskdef_id == 1:
            return run_summarise(file_path)

        elif taskdef_id == 2:
            return run_sentiment(file_path)

        else:
            return "[Unsupported Task]"
