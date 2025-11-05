# ==========================================
# File: agent_service.py
# Created in iteration: 1
# Author: Karl Concha
#
# #ChatGPT (OpenAI, 2025) – Assisted in structuring class methods for 
# linking DAO layers to Flask routing, refining CRUD aggregation logic, 
# and applying consistent FYP Bible documentation standards.
# Conversation Topic: "Rainn Iteration 1 – Service layer connecting DAO to Flask"
# Date: November 2025
#
# References:
# - SQLite Documentation – "Python SQLite3 Module" (https://docs.python.org/3/library/sqlite3.html)
# - Flask Documentation – "Application Factories and Service Layers" (https://flask.palletsprojects.com/)
# - UCC IS4470 FYP Bible – Iteration documentation and code referencing requirements.
# ==========================================

# Routing of all DAO functions to Flask

from dao.task_def_dao import TaskDefDAO
from dao.task_stage_def_dao import TaskStageDefDAO
from model.task_stage_def import TaskStageDef
from model.task_def import TaskDef


class AgentService:
    """ Provides a service layer between Flask routes and DAO classes. """

    def __init__(self):
        """ Initializes DAO instances for agent and stage management. """
        self.taskdef_dao = TaskDefDAO()
        self.taskstage_dao = TaskStageDefDAO()

    def create_agent_with_stages(self, name, description):
        """ Creates a TaskDef and adds default 3 stages (Input, Summarise, Output).
        ChatGPT suggested using helper DAO sequence for automatic stage insertion. """

        new_task = TaskDef(None, name, description)
        self.taskdef_dao.add_TaskDef(new_task)

        # Get the latest task we just added
        taskdefs = self.taskdef_dao.get_all_TaskDefs()
        task_id = taskdefs[-1].TaskDef_ID  # Retrieving the last item in the table

        # Default stages for demonstration
        stages = [
            TaskStageDef(None, task_id, "Input", "Upload CV files"),
            TaskStageDef(None, task_id, "Summarise", "Summarise CV content using AI"),
            TaskStageDef(None, task_id, "Output", "Display or export the summary results")
        ]

        for stage in stages:
            self.taskstage_dao.add_TaskStageDef(stage)

        return task_id

    def delete_agent(self, agent_id):
        """ Deletes an agent and all associated stages.
        ChatGPT assisted in loop-based cascade deletion approach. """
        stages = self.taskstage_dao.get_all_TaskStageDefs()
        for stage in stages:
            if stage.TaskDef_ID_FK == agent_id:
                self.taskstage_dao.delete_TaskStageDef(stage.TaskStageDef_ID)

        self.taskdef_dao.delete_TaskDef(agent_id)

    def update_agent_details(self, agent_id, name, description):
        """ Updates agent details in TaskDef table. """
        updated_agent = TaskDef(agent_id, name, description)
        self.taskdef_dao.update_TaskDef(updated_agent)

    def get_agent_by_id(self, agent_id):
        """ Retrieves a single agent by ID. """
        return self.taskdef_dao.get_TaskDef_by_id(agent_id)

    def get_agent_stages_by_id(self, agent_id):
        """ Retrieves stages belonging to a specific agent. """
        return self.taskstage_dao.get_TaskStageDef_by_id(agent_id)

    def list_agents(self):
        """ Returns all agents from the TaskDef table. """
        return self.taskdef_dao.get_all_TaskDefs()

    def list_stages(self):
        """ Returns all stages from the TaskStageDef table. """
        return self.taskstage_dao.get_all_TaskStageDefs()
