# ==========================================
# File: task_stage_instance_dao.py
# Updated in iteration: 4
# Author: Karl Concha
#
# Purpose:
# Data access layer for TaskStageInstance persistence.
#
# Notes:
# - One row per stage execution
# - Stores output artifact paths and error messages
# - Stage ordering is enforced via Stage_Order
# ==========================================

import sqlite3
from model.task_stage_instance import TaskStageInstance


class TaskStageInstanceDAO:

    def __init__(self, db_name="rainn.db"):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def create_stage_instance(self, stage_instance: TaskStageInstance):
        """Creates a TaskStageInstance row and returns its ID."""
        self.cursor.execute(
            """
            INSERT INTO TaskStageInstance
                (TaskInstance_ID_FK, Stage_Order, Stage_Name,
                 Status, Output_Artifact_Path, Started_At)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """,
            (
                stage_instance.TaskInstance_ID_FK,
                stage_instance.Stage_Order,
                stage_instance.Stage_Name,
                stage_instance.Status,
                stage_instance.Output_Artifact_Path
            )
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def mark_completed(self, stage_instance_id, output_artifact_path):
        """Marks a stage as completed and records its output artifact."""
        self.cursor.execute(
            """
            UPDATE TaskStageInstance
            SET Status = 'COMPLETED',
                Output_Artifact_Path = ?,
                Ended_At = CURRENT_TIMESTAMP
            WHERE TaskStageInstance_ID = ?
            """,
            (output_artifact_path, stage_instance_id)
        )
        self.connection.commit()

    def mark_failed(self, stage_instance_id, error_message):
        """Marks a stage as failed and stores the error message."""
        self.cursor.execute(
            """
            UPDATE TaskStageInstance
            SET Status = 'FAILED',
                Error_Message = ?,
                Ended_At = CURRENT_TIMESTAMP
            WHERE TaskStageInstance_ID = ?
            """,
            (error_message, stage_instance_id)
        )
        self.connection.commit()

    def get_stages_for_task_instance(self, task_instance_id_fk):
        """Returns all stage executions for a TaskInstance."""
        self.cursor.execute(
            """
            SELECT * FROM TaskStageInstance
            WHERE TaskInstance_ID_FK = ?
            ORDER BY Stage_Order ASC
            """,
            (task_instance_id_fk,)
        )
        rows = self.cursor.fetchall()

        return [
            TaskStageInstance(
                r["TaskStageInstance_ID"],
                r["TaskInstance_ID_FK"],
                r["Stage_Order"],
                r["Stage_Name"],
                r["Status"],
                r["Output_Artifact_Path"],
                r["Started_At"],
                r["Ended_At"],
                r["Error_Message"]
            )
            for r in rows
        ]

    def get_all_stage_instances(self):
        """Returns all TaskStageInstances (newest first)."""
        self.cursor.execute(
            "SELECT * FROM TaskStageInstance ORDER BY TaskStageInstance_ID DESC"
        )
        rows = self.cursor.fetchall()

        return [
            TaskStageInstance(
                row["TaskStageInstance_ID"],
                row["TaskInstance_ID_FK"],
                row["Stage_Order"],
                row["Stage_Name"],
                row["Status"],
                row["Output_Artifact_Path"],
                row["Started_At"],
                row["Ended_At"],
                row["Error_Message"]
            )
            for row in rows
        ]

    def clear_outputs_for_task_instance(self, task_instance_id_fk):
        """Clears output paths and error messages for a TaskInstance."""
        self.cursor.execute(
            """
            UPDATE TaskStageInstance
            SET Output_Artifact_Path = NULL,
                Error_Message = NULL
            WHERE TaskInstance_ID_FK = ?
            """,
            (task_instance_id_fk,)
        )
        self.connection.commit()

    def delete_for_task_instance(self, task_instance_id_fk):
        """Hard deletes TaskStageInstance rows for a TaskInstance."""
        self.cursor.execute(
            "DELETE FROM TaskStageInstance WHERE TaskInstance_ID_FK = ?",
            (task_instance_id_fk,)
        )
        self.connection.commit()

    def close_connection(self):
        self.connection.close()
