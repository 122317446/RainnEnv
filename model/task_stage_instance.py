# ==========================================
# File: task__stage_instance.py
# Updated in iteration: 3
# Author: Karl Concha
#
# Notes:
# Implemented in iteration 3 with slight changes of its attributes
# to fit the db schema
# ==========================================


class TaskStageInstance:
    """ Represents an instance of a stage associated with a specific task instance. """

    def __init__(self, TaskStageInstance_ID, TaskInstance_ID_FK, Stage_Order, Stage_Name, Status, Output_Artifact_Path, Started_At, Ended_At, Error_Message):
        """ Initializes TaskStageInstance attributes. """
        self.TaskStageInstance_ID = TaskStageInstance_ID
        self.TaskInstance_ID_FK = TaskInstance_ID_FK
        self.Stage_Order = Stage_Order
        self.Stage_Name = Stage_Name
        self.Status = Status
        self.Output_Artifact_Path = Output_Artifact_Path
        self.Started_At = Started_At
        self.Ended_At = Ended_At
        self.Error_Message = Error_Message
