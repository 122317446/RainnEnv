import sqlite3
from model.task_instance import TaskInstance


class TaskInstanceDAO:

    def __init__(self, db_name="rainn.db"):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def create_task_instance(self, process_id_fk, taskdef_id_fk, status, run_folder):
        """
        Creates a new TaskInstance row and returns its ID.
        """
        self.cursor.execute(
            """
            INSERT INTO TaskInstance
                (Process_ID_FK, TaskDef_ID_FK, Status, Run_Folder)
            VALUES (?, ?, ?, ?)
            """,
            (process_id_fk, taskdef_id_fk, status, run_folder)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def get_task_instance_by_id(self, task_instance_id):
        """
        Returns a TaskInstance object or None.
        """
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
        """
        Updates the status of a TaskInstance.
        """
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
        """
        Updates the run folder path.
        """
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
        """ Retrieves all TaskInstance records (newest first). """
        self.cursor.execute("SELECT * FROM TaskInstance ORDER BY TaskInstance_ID DESC")
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
