import sqlite3
from model.task_def import TaskDef

class TaskDefDAO:
    def __init__(self, db_name="rainn.db"):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS TaskDef (
                TaskDef_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                TaskDef_Name TEXT NOT NULL,
                TaskDef_Description TEXT
            )
        ''')
        self.connection.commit()

    def add_TaskDef(self, task_def):
        self.cursor.execute(
            '''INSERT INTO TaskDef (TaskDef_Name, TaskDef_Description)
               VALUES (?, ?)''',
            (task_def.TaskDef_Name, task_def.TaskDef_Description)
        )
        self.connection.commit()

    def get_all_TaskDefs(self):
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
        self.cursor.execute('''
            UPDATE TaskDef
            SET TaskDef_Name = ?, TaskDef_Description = ?
            WHERE TaskDef_ID = ?
        ''', (task_def.TaskDef_Name, task_def.TaskDef_Description, task_def.TaskDef_ID))
        self.connection.commit()

    def delete_TaskDef(self, TaskDef_ID):
        self.cursor.execute("DELETE FROM TaskDef WHERE TaskDef_ID = ?", (TaskDef_ID,))
        self.connection.commit()

    def close_connection(self):
        self.connection.close()
