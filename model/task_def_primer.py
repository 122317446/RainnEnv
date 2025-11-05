# ==========================================
# File: task_def_primer.py
# Created in iteration: 1
# Author: Karl Concha
#
# Notes:
# This model was introduced in Iteration 1 to serve as a placeholder for 
# future integration of agent primer data. 
# It has not been actively used or referenced in DAO classes as of Iteration 1. 
# It remains included for completeness and potential expansion in later iterations.
# ==========================================


class TaskDefPrimer:
    """ Represents a primer or initial configuration object for Task Definitions. """

    def __init__(self, TaskDefPrimer_ID, TaskDefPrimer_Description):
        """ Initializes TaskDefPrimer attributes. """
        self.TaskDefPrimer_ID = TaskDefPrimer_ID
        self.TaskDefPrimer_Description = TaskDefPrimer_Description

    def to_dict(self):
        """ Converts TaskDefPrimer instance to dictionary format. """
        return {
            "TaskDefPrimer_ID": self.TaskDefPrimer_ID,
            "TaskDefPrimer_Description": self.TaskDefPrimer_Description
        }
