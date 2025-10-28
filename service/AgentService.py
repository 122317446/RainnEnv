from DAO.AgentDAO import AgentDAO
class AgentService:
    def __init__(self):
        self.agent_dao = AgentDAO()
    
    def get_all_agents(self):
        return self.agent_dao.get_all_Userinputs()
    
    def get_agent_details(self, AgentID): 
        return self.agent_dao.get_Agent_by_id(AgentID)
    
    def add_agent(self, input): 
        return self.agent_dao.add_Agent(input)
    
    #def update_data(self, input): Unused in this iteration
        return self.agent_dao.update_Userinputs(input)
    
    def delete_agent(self, AgentID):
        return self.agent_dao.delete_Agent(AgentID)