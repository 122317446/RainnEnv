import sqlite3
from model.task_stage_def import TaskStageDef

class TaskStageDefDAO:
    def __init__(self, db_name="rainn.db"):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS TaskStageDef (
                TaskStageDef_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                TaskDef_ID_FK INTEGER,
                TaskStageDef_Type TEXT NOT NULL,
                TaskStageDef_Description TEXT,
                FOREIGN KEY (TaskDef_ID_FK) REFERENCES TaskDef(TaskDef_ID)
            )
        ''')
        self.connection.commit()

    def add_TaskStageDef(self, stage_def):
        self.cursor.execute(
            '''INSERT INTO TaskStageDef (
                TaskDef_ID_FK, TaskStageDef_Type, TaskStageDef_Description)
               VALUES (?, ?, ?)''',
            (stage_def.TaskDef_ID_FK, stage_def.TaskStageDef_Type, stage_def.TaskStageDef_Description)
        )
        self.connection.commit()

    def get_all_TaskStageDefs(self):
        self.cursor.execute("SELECT * FROM TaskStageDef")
        rows = self.cursor.fetchall()
        return [
            TaskStageDef(
                row["TaskStageDef_ID"],
                row["TaskDef_ID_FK"],
                row["TaskStageDef_Type"],
                row["TaskStageDef_Description"]
            )
            for row in rows
        ]

    def get_TaskStageDef_by_id(self, TaskStageDef_ID):
        self.cursor.execute("SELECT * FROM TaskStageDef WHERE TaskStageDef_ID = ?", (TaskStageDef_ID,))
        row = self.cursor.fetchone()
        if row:
            return TaskStageDef(
                row["TaskStageDef_ID"],
                row["TaskDef_ID_FK"],
                row["TaskStageDef_Type"],
                row["TaskStageDef_Description"]
            )
        else:
            return None

    def update_TaskStageDef(self, stage_def):
        self.cursor.execute('''
            UPDATE TaskStageDef
            SET TaskDef_ID_FK = ?, TaskStageDef_Type = ?, TaskStageDef_Description = ?
            WHERE TaskStageDef_ID = ?
        ''', (stage_def.TaskDef_ID_FK, stage_def.TaskStageDef_Type, stage_def.TaskStageDef_Description, stage_def.TaskStageDef_ID))
        self.connection.commit()

    def delete_TaskStageDef(self, TaskStageDef_ID):
        self.cursor.execute("DELETE FROM TaskStageDef WHERE TaskStageDef_ID = ?", (TaskStageDef_ID,))
        self.connection.commit()

    def close_connection(self):
        self.connection.close()
