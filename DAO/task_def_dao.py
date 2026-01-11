# ==========================================
# File: task_def_dao.py
# Created in iteration: 1
# Author: Karl Concha
#
# #ChatGPT (OpenAI, 2025) – Assisted in structuring CRUD methods for TaskDefDAO
# and ensuring compliance with the UCC FYP Bible documentation requirements.
# Conversation Topic: "Rainn Iteration 1 – Database CRUD setup with SQLite + Flask"
# Date: November 2025
#
# References:
# - SQLite Documentation – "Python SQLite3 Module" (https://docs.python.org/3/library/sqlite3.html)
# - Tutorial adapted: “CRUD Operations using SQLite3 in Python” – GeeksForGeeks
#   (https://www.geeksforgeeks.org/python-sqlite/)
# ==========================================

import sqlite3
from model.task_def import TaskDef


class TaskDefDAO:

    def __init__(self, db_name="rainn.db"):
        """ Initializes the connection to the SQLite database. """

        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def add_TaskDef(self, task_def):
        """ Inserts a new TaskDef record into the database. """

        self.cursor.execute(
            '''INSERT INTO TaskDef (TaskDef_Name, TaskDef_Description)
               VALUES (?, ?)''',
            (task_def.TaskDef_Name, task_def.TaskDef_Description)
        )
        self.connection.commit()

    def get_all_TaskDefs(self):
        """ Retrieves all TaskDef records from the database.
        Returns a list of TaskDef objects.
        ChatGPT assisted in structuring list comprehension for cleaner mapping. """

        self.cursor.execute("SELECT * FROM TaskDef")
        rows = self.cursor.fetchall()
        return [
            TaskDef(
                row["TaskDef_ID"],
                row["TaskDef_Name"],
                row["TaskDef_Description"]
            )
            for row in rows
        ]

    def get_TaskDef_by_id(self, TaskDef_ID):
        """ Retrieves a TaskDef record by its ID.
        ChatGPT confirmed use of parameter substitution syntax in SELECT queries. """

        self.cursor.execute("SELECT * FROM TaskDef WHERE TaskDef_ID = ?", (TaskDef_ID,))
        row = self.cursor.fetchone()
        if row:
            return TaskDef(
                row["TaskDef_ID"],
                row["TaskDef_Name"],
                row["TaskDef_Description"]
            )
        else:
            return None

    def update_TaskDef(self, task_def):
        """ Updates an existing TaskDef record.
        ChatGPT assisted in refining UPDATE syntax and commit handling. """
        self.cursor.execute('''
            UPDATE TaskDef
            SET TaskDef_Name = ?, TaskDef_Description = ?
            WHERE TaskDef_ID = ?
        ''', (task_def.TaskDef_Name, task_def.TaskDef_Description, task_def.TaskDef_ID))
        self.connection.commit()

    def delete_TaskDef(self, TaskDef_ID):
        """ Deletes a TaskDef record by its ID. """
        self.cursor.execute("DELETE FROM TaskDef WHERE TaskDef_ID = ?", (TaskDef_ID,))
        self.connection.commit()

    def close_connection(self):
        """ Closes the SQLite database connection. """
        self.connection.close()
