import sqlite3
from model.Agent import Agent


class AgentDAO:
    def __init__(self, db_name="agent.db"):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS AgentTable (
                        AgentID INTEGER PRIMARY KEY AUTOINCREMENT,
                        AgentName TEXT NOT NULL, 
                        AgentModel TEXT NOT NULL,
                        AgentTask TEXT NOT NULL)
                            ''')
        self.connection.commit()

    def add_Agent(self, Agent):
        self.cursor.execute(
            '''INSERT INTO AgentTable (
                        AgentName, AgentModel, AgentTask)
            VALUES (?, ?, ?)''',
            (Agent.AgentName, Agent.AgentModel, Agent.AgentTask,)
        )
        self.connection.commit()

    def get_all_Agents(self):
        self.cursor.execute("SELECT * FROM AgentTable")
        agents = self.cursor.fetchall()
        return agents
    
    def get_Agent_by_id(self, AgentID):
        self.cursor.execute("SELECT * FROM AgentTable WHERE AgentID = ?", (AgentID,))
        row = self.cursor.fetchone()
        if row:
            return Agent(row[0], row[1], row[2], row[3])
        else:
            return None

    #def update_Userinputs(self, Userinputs): Unused as of current iteration
        self.cursor.execute('''
                            UPDATE Userinputs
                            SET text = ? WHERE ID = ?
                            ''', (Userinputs.text, Userinputs.ID))
        self.connection.commit()

    def delete_Agent(self, AgentID):
        self.cursor.execute("Delete FROM AgentTable WHERE AgentID = ?", (AgentID,))
        self.connection.commit()
        self.connection.close()

    def close_connection(self):
        self.connection.close()