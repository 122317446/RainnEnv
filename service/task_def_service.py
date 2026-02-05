# ==========================================
# File: taskdef_service.py
# Updated in iteration: 4
# Author: Karl Concha
#
# #ChatGPT (OpenAI, 2025) – Assisted in refactoring the service layer by 
# splitting TaskDef responsibilities from AgentService into a dedicated 
# modular class, following clean architecture and FYP Bible standards.
# Conversation Topic: "Refactoring Rainn – Splitting TaskDef service logic"
# Date: November 2025
#
# References:
# - SQLite3 Documentation – https://docs.python.org/3/library/sqlite3.html
# - Flask Service Layer Patterns – https://flask.palletsprojects.com/
# - UCC IS4470 FYP Bible – Code modularity + documentation guidelines
# ==========================================

from dao.task_def_dao import TaskDefDAO
from model.task_def import TaskDef

class TaskDefService:
    """ Provides a service layer dedicated to TaskDef management. """

    def __init__(self):
        """ Initializes DAO instance for TaskDef operations. """
        self.taskdef_dao = TaskDefDAO()

    def create_taskdef(self, name, description):
        """ Creates a new TaskDef (agent type). """
        new_task = TaskDef(None, name, description)
        created = self.taskdef_dao.add_TaskDef(new_task)
        return created.TaskDef_ID

    def get_taskdef_by_id(self, taskdef_id):
        """ Retrieves a TaskDef by its ID. """
        return self.taskdef_dao.get_TaskDef_by_id(taskdef_id)

    def list_taskdefs(self):
        """ Returns all TaskDefs in the system. """
        return self.taskdef_dao.get_all_TaskDefs()

    def update_taskdef(self, taskdef_id, name, description):
        """ Updates an existing TaskDef entry. """
        updated_task = TaskDef(taskdef_id, name, description)
        return self.taskdef_dao.update_TaskDef(updated_task)

    def delete_taskdef(self, taskdef_id):
        """ Deletes a TaskDef entry. """
        return self.taskdef_dao.delete_TaskDef(taskdef_id)
