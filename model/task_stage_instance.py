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
