# ==========================================
# File: task_stage_instance.py
# Created in iteration: 1
# Author: Karl Concha
#
# Notes:
# This model was introduced in Iteration 1 to represent individual task stage instances 
# linked to Task Instances. 
# It has not been actively used or connected to DAO logic as of Iteration 1, 
# but is retained for completeness and planned integration in later iterations.
# ==========================================


class TaskStageInstance:
    """ Represents an instance of a stage associated with a specific task instance. """

    def __init__(self, TaskStageInstance_ID, TaskInstance_ID_FK, TaskStageInstance_Status, TaskStageInstance_Type):
        """ Initializes TaskStageInstance attributes. """
        self.TaskStageInstance_ID = TaskStageInstance_ID
        self.TaskInstance_ID_FK = TaskInstance_ID_FK
        self.TaskStageInstance_Status = TaskStageInstance_Status
        self.TaskStageInstance_Type = TaskStageInstance_Type

    def to_dict(self):
        """ Converts TaskStageInstance instance to dictionary format. """
        return {
            "TaskStageInstance_ID": self.TaskStageInstance_ID,
            "TaskInstance_ID_FK": self.TaskInstance_ID_FK,
            "TaskStageInstance_Status": self.TaskStageInstance_Status,
            "TaskStageInstance_Type": self.TaskStageInstance_Type
        }
