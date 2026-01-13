# ==========================================
# File: agent_process_dao.py
# Created in iteration: 2
# Author: Karl Concha
#
# #ChatGPT (OpenAI, 2025) – Assisted in renaming DAO to match
# new AgentProcess table structure following supervisor guidance.
# Conversation Topic: "Refactoring Rainn DAO – AgentProcess"
# Date: November 2025
#
# References:
# - SQLite3 Documentation – https://docs.python.org/3/library/sqlite3.html
# - UCC IS4470 FYP Bible – DAO patterns + Python standards
# ==========================================

import sqlite3
from model.agent_process import AgentProcess


class AgentProcessDAO:
    """ DAO class for CRUD operations on the AgentProcess table. """

    def __init__(self, db_name="rainn.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def add_AgentProcess(self, process):
        """ Inserts a new AgentProcess record. """
        self.cursor.execute("""
            INSERT INTO AgentProcess (User_ID, Agent_Name, Agent_Priming, AI_Model, Operation_Selected)
            VALUES (?, ?, ?, ?, ?)
        """, (process.User_ID, process.Agent_Name, process.Agent_Priming, process.AI_Model, process.Operation_Selected))

        self.conn.commit()
        process.Process_ID = self.cursor.lastrowid
        return process

    def get_AgentProcess_by_id(self, process_id):
        self.cursor.execute(
            "SELECT * FROM AgentProcess WHERE Process_ID = ?",
            (process_id,)
        )
        row = self.cursor.fetchone()
        if not row:
            return None

        return AgentProcess(
            row["Process_ID"],
            row["User_ID"],
            row["Agent_Name"],
            row["Agent_Priming"],
            row["AI_Model"],
            row["Operation_Selected"],
            row["Created_At"]
        )

    def get_all_AgentProcesses(self):
        """ Returns all AgentProcess entries ordered by newest first. """

        self.cursor.execute(
            "SELECT * FROM AgentProcess ORDER BY Created_At DESC"
        )
        rows = self.cursor.fetchall()

        return [
            AgentProcess(
                r["Process_ID"],
                r["User_ID"],
                r["Agent_Name"],
                r["Agent_Priming"],
                r["AI_Model"],
                r["Operation_Selected"],
                r["Created_At"]
            )
            for r in rows
        ]

    def update_AgentProcess(self, process):
        """ Updates an existing AgentProcess record. """

        self.cursor.execute(
            '''
            UPDATE AgentProcess
            SET 
                User_ID = ?,
                Agent_Name = ?,
                Agent_Priming = ?,
                AI_Model = ?,
                Operation_Selected = ?
            WHERE Process_ID = ?
            ''',
            (
                process.User_ID,
                process.Agent_Name,
                process.Agent_Priming,
                process.AI_Model,
                process.Operation_Selected,
                process.Process_ID
            )
        )

        self.conn.commit()

    def delete_AgentProcess(self, process_id):
        """ Deletes an AgentProcess entry by its ID. """
        self.cursor.execute(
            "DELETE FROM AgentProcess WHERE Process_ID = ?", 
            (process_id,)
        )
        self.conn.commit()

    def close(self):
        """ Closes the database connection. """
        self.conn.close()
