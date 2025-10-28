from DAO.AgentDAO import AgentDAO
from model.Agent import Agent

def inject_sample_data():
    inject_agent_dao = AgentDAO(db_name="agent.db")

    example1 = Agent(None, 'Stewart', 'Ollama', 'Pathfinder')
    inject_agent_dao.add_Agent(example1)

    inject_agent_dao.close_connection()

    print("Sample data has been added to the database!")
    

if __name__ == "__main__":
    inject_sample_data()

