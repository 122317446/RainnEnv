class TaskDef:
   
    def __init__(self, TaskDef_ID, TaskDef_Name, TaskDef_Description):

        self.TaskDef_ID = TaskDef_ID
        self.TaskDef_Name = TaskDef_Name
        self.TaskDef_Description = TaskDef_Description

    def to_dict(self):
        return {
            "TaskDef_ID": self.TaskDef_ID,
            "TaskDef_Name": self.TaskDef_Name,
            "TaskDef_Description": self.TaskDef_Description
        }