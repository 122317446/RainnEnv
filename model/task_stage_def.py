# ==========================================
# File: task_stage_def.py
# Created in iteration: 1
# Author: Karl Concha
# ==========================================


class TaskStageDef:
    """ Represents a stage or step definition linked to a Task Definition. """

    def __init__(self, TaskStageDef_ID, TaskDef_ID_FK, TaskStageDef_Type, TaskStageDef_Description):
        """ Initializes TaskStageDef attributes. """
        self.TaskStageDef_ID = TaskStageDef_ID
        self.TaskDef_ID_FK = TaskDef_ID_FK
        self.TaskStageDef_Type = TaskStageDef_Type
        self.TaskStageDef_Description = TaskStageDef_Description

    def to_dict(self):
        """ Converts TaskStageDef instance to dictionary format. """
        return {
            "TaskStageDef_ID": self.TaskStageDef_ID,
            "TaskDef_ID_FK": self.TaskDef_ID_FK,
            "TaskStageDef_Type": self.TaskStageDef_Type,
            "TaskStageDef_Description": self.TaskStageDef_Description
        }
