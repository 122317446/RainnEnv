# ==========================================
# File: taskstage_service.py
# Created in iteration: 2
# Author: Karl Concha
#
# #ChatGPT (OpenAI, 2025) – Assisted in restructuring stage-handling logic
# into a dedicated TaskStageDef service class to comply with modular FYP 
# guidelines and improve maintainability.
# Conversation Topic: "Splitting Rainn TaskStage service layer"
# Date: November 2025
#
# References:
# - SQLite3 Documentation – https://docs.python.org/3/library/sqlite3.html
# - DAO/Service Design Patterns – https://flask.palletsprojects.com/
# - UCC IS4470 FYP Bible – Modularity + documentation standards
# ==========================================

from dao.task_stage_def_dao import TaskStageDefDAO
from model.task_stage_def import TaskStageDef

class TaskStageService:
    """ Provides a service layer dedicated to TaskStageDef management. """

    def __init__(self):
        """ Initializes DAO instance for TaskStageDef operations. """
        self.taskstage_dao = TaskStageDefDAO()

    def create_stage(self, taskdef_id, stage_type, description):
        """ Creates a new stage for a specific TaskDef. """
        new_stage = TaskStageDef(None, taskdef_id, stage_type, description)
        return self.taskstage_dao.add_TaskStageDef(new_stage)

    def get_stages_for_task(self, taskdef_id):
        """ Retrieves all stages belonging to a specific TaskDef. """
        return self.taskstage_dao.get_TaskStageDef_by_id(taskdef_id)

    def list_all_stages(self):
        """ Returns all TaskStageDef entries in the system. """
        return self.taskstage_dao.get_all_TaskStageDefs()

    def delete_stage(self, stage_id):
        """ Deletes a single TaskStageDef. """
        return self.taskstage_dao.delete_TaskStageDef(stage_id)

    def delete_stages_for_task(self, taskdef_id):
        """ Deletes all stages associated with a given TaskDef. """
        stages = self.taskstage_dao.get_all_TaskStageDefs()
        for s in stages:
            if s.TaskDef_ID_FK == taskdef_id:
                self.taskstage_dao.delete_TaskStageDef(s.TaskStageDef_ID)
