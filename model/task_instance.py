# ==========================================
# File: task_instance.py
# Updated in iteration: 3
# Author: Karl Concha
#
# Notes:
# Implemented in iteration 3 with slight changes of its attributes
# to fit the db schema
# ==========================================


class TaskInstance:
    """ Represents an instance of a task derived from a Task Definition. """

    def __init__(
        self,
        TaskInstance_ID,
        Process_ID_FK,
        TaskDef_ID_FK,
        Status,
        Run_Folder,
        Last_Accessed_At,
        Expires_At,
        Deleted_At,
        Downloaded_At,
        Created_At,
        Updated_At
    ):
        """ Initializes TaskInstance attributes. """
        self.TaskInstance_ID = TaskInstance_ID
        self.Process_ID_FK = Process_ID_FK
        self.TaskDef_ID_FK = TaskDef_ID_FK
        self.Status = Status
        self.Run_Folder = Run_Folder
        self.Last_Accessed_At = Last_Accessed_At
        self.Expires_At = Expires_At
        self.Deleted_At = Deleted_At
        self.Downloaded_At = Downloaded_At
        self.Created_At = Created_At
        self.Updated_At = Updated_At
