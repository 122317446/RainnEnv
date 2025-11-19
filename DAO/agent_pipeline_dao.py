# ==========================================
# File: agent_pipeline_dao.py
# Created in iteration: 2
# Author: Karl Concha
#
# #ChatGPT (OpenAI, 2025) – Assisted in refactoring DAO to match new 
# AgentPipeline table structure, correcting naming, and improving CRUD 
# consistency according to FYP Bible guidelines.
# Conversation Topic: "Refactoring Rainn DAO – AgentPipeline"
# Date: November 2025
#
# References:
# - SQLite3 Documentation – https://docs.python.org/3/library/sqlite3.html
# - UCC IS4470 FYP Bible – DAO patterns + Python standards
# ==========================================

import sqlite3
from model.agent_pipeline import AgentPipeline


class AgentPipelineDAO:
    """ DAO class for CRUD operations on the AgentPipeline table. """

    def __init__(self, db_name="rainn.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    # ---------------------------------------------------
    # CREATE
    # ---------------------------------------------------
    def add_AgentPipeline(self, pipeline):
        self.cursor.execute("""
            INSERT INTO AgentPipeline (User_ID, Agent_Name, Operation_Selected)
            VALUES (?, ?, ?)
        """, (pipeline.User_ID, pipeline.Agent_Name, pipeline.Operation_Selected))

        self.conn.commit()
        pipeline.Pipeline_ID = self.cursor.lastrowid
        return pipeline


    # ---------------------------------------------------
    # READ BY ID
    # ---------------------------------------------------
    def get_AgentPipeline_by_id(self, pipeline_id):
        self.cursor.execute(
            "SELECT * FROM AgentPipeline WHERE Pipeline_ID = ?",
            (pipeline_id,)
        )
        row = self.cursor.fetchone()
        if not row:
            return None

        return AgentPipeline(
            row["Pipeline_ID"],
            row["User_ID"],
            row["Agent_Name"],
            row["Operation_Selected"],
            row["Created_At"]
        )


    # ---------------------------------------------------
    # READ ALL
    # ---------------------------------------------------
    def get_all_AgentPipelines(self):
        """ Returns all agent pipeline entries ordered by newest first. """

        self.cursor.execute(
            "SELECT * FROM AgentPipeline ORDER BY Created_At DESC"
        )
        rows = self.cursor.fetchall()

        return [
            AgentPipeline(
                r["Pipeline_ID"],
                r["User_ID"],
                r["Agent_Name"],
                r["Operation_Selected"],
                r["Created_At"]
            )
            for r in rows
        ]

    # ---------------------------------------------------
    # UPDATE
    # ---------------------------------------------------
    def update_AgentPipeline(self, agent_pipeline):
        """ Updates an existing AgentPipeline record. """

        self.cursor.execute(
            '''
            UPDATE AgentPipeline
            SET 
                User_ID = ?,
                Agent_Name = ?,
                Operation_Selected = ?
            WHERE Pipeline_ID = ?
            ''',
            (
                agent_pipeline.User_ID,
                agent_pipeline.Agent_Name,
                agent_pipeline.Operation_Selected,
                agent_pipeline.Pipeline_ID
            )
        )

        self.conn.commit()

    # ---------------------------------------------------
    # DELETE
    # ---------------------------------------------------
    def delete_AgentPipeline(self, pipeline_id):
        """ Deletes an AgentPipeline entry by its ID. """
        self.cursor.execute(
            "DELETE FROM AgentPipeline WHERE Pipeline_ID = ?", 
            (pipeline_id,)
        )
        self.conn.commit()

    # ---------------------------------------------------
    # CLOSE CONNECTION
    # ---------------------------------------------------
    def close(self):
        """ Closes the database connection. """
        self.conn.close()
