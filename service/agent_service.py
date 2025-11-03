# routing of all dao functions to flask
from dao.task_def_dao import TaskDefDAO
from dao.task_stage_def_dao import TaskStageDefDAO
from model.task_stage_def import TaskStageDef 
from model.task_def import TaskDef

class AgentService:
    def __init__(self):
        self.taskdef_dao = TaskDefDAO()
        self.taskstage_dao = TaskStageDefDAO()

    def create_agent_with_stages(self, name, description):
        """Create a TaskDef and add default 3 stages (Input, Summarise, Output)."""
        new_task = TaskDef(None, name, description)
        self.taskdef_dao.add_TaskDef(new_task)

        # Get the latest task we just added
        taskdefs = self.taskdef_dao.get_all_TaskDefs()
        task_id = taskdefs[-1].TaskDef_ID #Retreiving the last item in the table

        # Default stages for demo
        stages = [
            TaskStageDef(None, task_id, "Input", "Upload CV files"),
            TaskStageDef(None, task_id, "Summarise", "Summarise CV content using AI"),
            TaskStageDef(None, task_id, "Output", "Display or export the summary results")
        ]
        for x in stages:
            self.taskstage_dao.add_TaskStageDef(x)

        return task_id

    def list_agents(self):
        """Return all TaskDefs."""
        return self.taskdef_dao.get_all_TaskDefs()

    def list_stages(self):
        """Return all TaskStageDefs."""
        return self.taskstage_dao.get_all_TaskStageDefs()
