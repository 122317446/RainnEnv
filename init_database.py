from DAO.AgentDAO import AgentDAO

def initialise_database():
    init_agent_DAO = AgentDAO(db_name="agent.db")

    print("The Agent DB is initalised!")

    init_agent_DAO.close_connection()


if __name__ == "__main__":
    initialise_database()