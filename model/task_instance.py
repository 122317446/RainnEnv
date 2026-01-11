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

    def __init__(self, TaskInstance_ID, Process_ID_FK, TaskDef_ID_FK, Status, Run_Folder, Created_At, Updated_At):
        """ Initializes TaskInstance attributes. """
        self.TaskInstance_ID = TaskInstance_ID
        self.Process_ID_FK = Process_ID_FK
        self.TaskDef_ID_FK = TaskDef_ID_FK
        self.Status = Status
        self.Run_Folder = Run_Folder
        self.Created_At = Created_At
        self.Updated_At = Updated_At
