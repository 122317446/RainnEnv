# ==========================================
# File: task_def.py
# Created in iteration: 1
# Author: Karl Concha
# ==========================================


class TaskDef:
    """ Represents a Task Definition entity within the Rainn system. """

    def __init__(self, TaskDef_ID, TaskDef_Name, TaskDef_Description):
        """ Initializes TaskDef attributes. """
        self.TaskDef_ID = TaskDef_ID
        self.TaskDef_Name = TaskDef_Name
        self.TaskDef_Description = TaskDef_Description

    def to_dict(self):
        """ Converts TaskDef instance into a dictionary format. """
        return {
            "TaskDef_ID": self.TaskDef_ID,
            "TaskDef_Name": self.TaskDef_Name,
            "TaskDef_Description": self.TaskDef_Description
        }
