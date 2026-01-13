# ==========================================
# File: agent_process.py
# Created in iteration: 2
# Author: Karl Concha

# Notes:
# agent_process is the created 'flow' the user builds.
# Instances will be applied in later iterations.
# ==========================================

class AgentProcess:

    def __init__(self, Process_ID, User_ID, Agent_Name, Agent_Priming, AI_Model,
                 Operation_Selected, Created_At):
        
        self.Process_ID = Process_ID
        self.User_ID = User_ID
        self.Agent_Name = Agent_Name
        self.Agent_Priming = Agent_Priming
        self.AI_Model = AI_Model
        self.Operation_Selected = Operation_Selected
        self.Created_At = Created_At