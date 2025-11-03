class TaskStageDef:
   
    def __init__(self, TaskStageDef_ID, TaskDef_ID_FK, TaskStageDef_Type, TaskStageDef_Description):

        self.TaskStageDef_ID = TaskStageDef_ID
        self.TaskDef_ID_FK = TaskDef_ID_FK
        self.TaskStageDef_Type = TaskStageDef_Type
        self.TaskStageDef_Description = TaskStageDef_Description

    def to_dict(self):
        return {
            "TaskStageDef_ID ": self.TaskStageDef_ID,
            "TaskDef_ID_FK": self.TaskDef_ID_FK,
            "TaskStageDef_Type": self.TaskStageDef_Type,
            "TaskStageDef_Description": self.TaskStageDef_Description
        }