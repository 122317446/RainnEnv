# ==========================================
# File: task_instance_dao.py
# Created in iteration: 3 
# Author: Karl Concha
#
# Data access layer for TaskInstance persistence.
#
# Notes:
# - Handles CRUD operations for execution runs
# - Uses SQLite timestamps for Created_At / Updated_At
# - Keeps logic intentionally simple and transparent
# ==========================================

import sqlite3
from model.task_instance import TaskInstance


class TaskInstanceDAO:

    def __init__(self, db_name="rainn.db"):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def create_task_instance(self, task_instance: TaskInstance):
        """Creates a new TaskInstance row and returns its ID."""
        self.cursor.execute(
            """
            INSERT INTO TaskInstance
                (Process_ID_FK, TaskDef_ID_FK, Status, Run_Folder)
            VALUES (?, ?, ?, ?)
            """,
            (
                task_instance.Process_ID_FK,
                task_instance.TaskDef_ID_FK,
                task_instance.Status,
                task_instance.Run_Folder
            )
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def get_task_instance_by_id(self, task_instance_id):
        """Fetches a TaskInstance by primary key."""
        self.cursor.execute(
            "SELECT * FROM TaskInstance WHERE TaskInstance_ID = ?",
            (task_instance_id,)
        )
        row = self.cursor.fetchone()
        if not row:
            return None

        return TaskInstance(
            row["TaskInstance_ID"],
            row["Process_ID_FK"],
            row["TaskDef_ID_FK"],
            row["Status"],
            row["Run_Folder"],
            row["Created_At"],
            row["Updated_At"]
        )

    def update_status(self, task_instance_id, status):
        """Updates execution status and timestamp."""
        self.cursor.execute(
            """
            UPDATE TaskInstance
            SET Status = ?, Updated_At = CURRENT_TIMESTAMP
            WHERE TaskInstance_ID = ?
            """,
            (status, task_instance_id)
        )
        self.connection.commit()

    def update_run_folder(self, task_instance_id, run_folder):
        """Persists the filesystem run folder path."""
        self.cursor.execute(
            """
            UPDATE TaskInstance
            SET Run_Folder = ?, Updated_At = CURRENT_TIMESTAMP
            WHERE TaskInstance_ID = ?
            """,
            (run_folder, task_instance_id)
        )
        self.connection.commit()

    def get_all_task_instances(self):
        """Returns all TaskInstances (newest first)."""
        self.cursor.execute(
            "SELECT * FROM TaskInstance ORDER BY TaskInstance_ID DESC"
        )
        rows = self.cursor.fetchall()

        return [
            TaskInstance(
                row["TaskInstance_ID"],
                row["Process_ID_FK"],
                row["TaskDef_ID_FK"],
                row["Status"],
                row["Run_Folder"],
                row["Created_At"],
                row["Updated_At"]
            )
            for row in rows
        ]

    def close_connection(self):
        self.connection.close()
