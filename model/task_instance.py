class TaskInstance:
   
    def __init__(self, TaskInstance_ID, TaskDef_ID_FK, TaskInstance_Start, TaskInstance_End, TaskInstance_Status):

        self.TaskInstance_ID = TaskInstance_ID
        self.TaskDef_ID_FK = TaskDef_ID_FK
        self.TaskInstance_Start = TaskInstance_Start
        self.TaskInstance_End = TaskInstance_End
        self.TaskInstance_Status = TaskInstance_Status

    def to_dict(self):
        return {
            "TaskInstance_ID ": self.TaskInstance_ID,
            "TaskDef_ID_FK": self.TaskDef_ID_FK,
            "TaskInstance_Start": self.TaskInstance_Start,
            "TaskInstance_End": self.TaskInstance_End,
            "TaskInstance_Status": self.TaskInstance_Status
        }