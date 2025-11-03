class TaskDefPrimer:
   
    def __init__(self, TaskDefPrimer_ID, TaskDefPrimer_Description):

        self.TaskDefPrimer_ID = TaskDefPrimer_ID
        self.TaskDefPrimer_Description = TaskDefPrimer_Description

    def to_dict(self):
        return {
            "TaskDefPrimer_ID ": self.TaskDefPrimer_ID,
            "TaskDefPrimer_Description": self.TaskDefPrimer_Description
        }