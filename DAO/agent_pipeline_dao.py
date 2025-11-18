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
    def add_AgentPipeline(self, agent_pipeline):
        """ Inserts a new AgentPipeline record into the database. """

        self.cursor.execute(
            '''
            INSERT INTO AgentPipeline
            (User_ID, Agent_Name, Text_Input, File_Text, Operation_Selected, Directory_Path)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (
                agent_pipeline.User_ID,
                agent_pipeline.Agent_Name,
                agent_pipeline.Text_Input,
                agent_pipeline.File_Text,
                agent_pipeline.Operation_Selected,
                agent_pipeline.Directory_Path
            )
        )

        self.conn.commit()
        agent_pipeline.Input_ID = self.cursor.lastrowid
        return agent_pipeline

    # ---------------------------------------------------
    # READ BY ID
    # ---------------------------------------------------
    def get_AgentPipeline_by_id(self, pipeline_id):
        """ Retrieves a single pipeline entry by its ID. """

        self.cursor.execute(
            "SELECT * FROM AgentPipeline WHERE Input_ID = ?", (pipeline_id,)
        )
        row = self.cursor.fetchone()

        if not row:
            return None

        return AgentPipeline(
            row["Input_ID"],
            row["User_ID"],
            row["Agent_Name"],
            row["Text_Input"],
            row["File_Text"],
            row["Operation_Selected"],
            row["Directory_Path"],
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
                r["Input_ID"],
                r["User_ID"],
                r["Agent_Name"],
                r["Text_Input"],
                r["File_Text"],
                r["Operation_Selected"],
                r["Directory_Path"],
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
                Text_Input = ?,
                File_Text = ?,
                Operation_Selected = ?,
                Directory_Path = ?
            WHERE Input_ID = ?
            ''',
            (
                agent_pipeline.User_ID,
                agent_pipeline.Agent_Name,
                agent_pipeline.Text_Input,
                agent_pipeline.File_Text,
                agent_pipeline.Operation_Selected,
                agent_pipeline.Directory_Path,
                agent_pipeline.Input_ID
            )
        )

        self.conn.commit()

    # ---------------------------------------------------
    # DELETE
    # ---------------------------------------------------
    def delete_AgentPipeline(self, pipeline_id):
        """ Deletes an AgentPipeline entry by its ID. """
        self.cursor.execute(
            "DELETE FROM AgentPipeline WHERE Input_ID = ?", 
            (pipeline_id,)
        )
        self.conn.commit()

    # ---------------------------------------------------
    # CLOSE CONNECTION
    # ---------------------------------------------------
    def close(self):
        """ Closes the database connection. """
        self.conn.close()
