class TaskStageInstance:
   
    def __init__(self, TaskStageInstance_ID, TaskInstance_ID_FK, TaskStageInstance_Status, TaskStageInstance_Type):

        self.TaskStageInstance_ID = TaskStageInstance_ID
        self.TaskInstance_ID_FK = TaskInstance_ID_FK
        self.TaskStageInstance_Status = TaskStageInstance_Status
        self.TaskStageInstance_Type = TaskStageInstance_Type

    def to_dict(self):
        return {
            "TaskStageInstance_ID": self.TaskStageInstance_ID,
            "TaskInstance_ID_FK": self.TaskInstance_ID_FK,
            "TaskStageInstance_Status": self.TaskStageInstance_Status,
            "TaskStageInstance_Type": self.TaskStageInstance_Type
        }