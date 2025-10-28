class Agent:

    def __init__(self, AgentID, AgentName, AgentModel, AgentTask):
        
        self.AgentID = AgentID
        self.AgentName = AgentName
        self.AgentModel = AgentModel
        self.AgentTask = AgentTask

    def to_dict(self):
        return {
            "AgentID": self.AgentID,
            "AgentName": self.AgentName,
            "AgentModel": self.AgentModel,
            "AgentTask": self.AgentTask
        }