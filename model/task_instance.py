# ==========================================
# File: task_instance.py
# Created in iteration: 1
# Author: Karl Concha
#
# Notes:
# This model was introduced in Iteration 1 as a placeholder for 
# managing task instances linked to Task Definitions. 
# It has not been actively used or referenced in DAO classes as of Iteration 1. 
# It remains included for completeness and potential expansion in later iterations.
# ==========================================


class TaskInstance:
    """ Represents an instance of a task derived from a Task Definition. """

    def __init__(self, TaskInstance_ID, TaskDef_ID_FK, TaskInstance_Start, TaskInstance_End, TaskInstance_Status):
        """ Initializes TaskInstance attributes. """
        self.TaskInstance_ID = TaskInstance_ID
        self.TaskDef_ID_FK = TaskDef_ID_FK
        self.TaskInstance_Start = TaskInstance_Start
        self.TaskInstance_End = TaskInstance_End
        self.TaskInstance_Status = TaskInstance_Status

    def to_dict(self):
        """ Converts TaskInstance instance to dictionary format. """
        return {
            "TaskInstance_ID": self.TaskInstance_ID,
            "TaskDef_ID_FK": self.TaskDef_ID_FK,
            "TaskInstance_Start": self.TaskInstance_Start,
            "TaskInstance_End": self.TaskInstance_End,
            "TaskInstance_Status": self.TaskInstance_Status
        }
