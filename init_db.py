# ==========================================
# File: init_db.py
# Updated in iteration: 2
# Author: Karl Concha
#
# #ChatGPT (OpenAI, 2025) – Assisted in updating schema
# to replace AgentPipeline → AgentProcess for consistency.
# ==========================================

import sqlite3

def init_db():
    conn = sqlite3.connect("rainn.db")
    cursor = conn.cursor()

    # DROP OLD TABLES
    cursor.execute("DROP TABLE IF EXISTS TaskStageDef")
    cursor.execute("DROP TABLE IF EXISTS TaskDef")
    cursor.execute("DROP TABLE IF EXISTS AgentProcess")
    cursor.execute("Drop TABLE IF EXISTS TaskInstance")
    cursor.execute("Drop TABLE IF EXISTS TasksStageInstance")

    # TaskDef Table
    cursor.execute("""
        CREATE TABLE TaskDef (
            TaskDef_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            TaskDef_Name TEXT NOT NULL UNIQUE,
            TaskDef_Description TEXT
        );
    """)

    # TaskStageDef Table
    cursor.execute("""
        CREATE TABLE TaskStageDef (
            TaskStageDef_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            TaskDef_ID_FK INTEGER,
            TaskStageDef_Type TEXT,
            TaskStageDef_Description TEXT,
            FOREIGN KEY (TaskDef_ID_FK) REFERENCES TaskDef(TaskDef_ID)
        );
    """)

    # TaskInstance Table (NEW Iteration 3, UserID not implemented)
    cursor.execute("""
        CREATE TABLE TaskInstance (
            TaskInstance_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Process_ID_FK INTEGER NOT NULL,
            TaskDef_ID_FK INTEGER NOT NULL,
            Status TEXT CHECK(Status IN ('RUNNING', 'COMPLETED', 'FAILED')) NOT NULL,
            Run_Folder TEXT NOT NULL,
            Created_At DATETIME DEFAULT CURRENT_TIMESTAMP,
            Updated_At DATETIME DEFAULT CURRENT_TIMESTAMP,
                   
            FOREIGN KEY (Process_ID_FK) REFERENCES Process(Process_ID),
            FOREIGN KEY (TaskDef_ID_FK) References Task(TaskDef_ID)

        );
    """)
    # Implementing Instances will now enable Rainn to represent scenario of
    # User X ran Process Y (using TaskDef Z) at time T.


    # TaskStageInstance Table (NEW Iteration 3)
    cursor.execute("""
        CREATE TABLE TaskStageInstance (
            TaskStageInstance_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            TaskInstance_ID_FK INTEGER NOT NULL,
            Stage_Order INTEGER NOT NULL,
            Stage_Name TEXT NOT NULL,
            Status TEXT CHECK(Status IN ('PENDING', 'RUNNING', 'COMPLETED', 'FAILED')) NOT NULL,
            Output_Artifact_Path TEXT,
            Started_At DATETIME,
            Ended_At DATETIME,
            Error_Message TEXT,
                   
            FOREIGN KEY (TaskInstance_ID_FK) REFERENCES TaskInstance(TaskInstance_ID)

        );
    """)
    # Implementing Stage Instances represents "Stage A of TaskInstance N produced artifact D and succeeded"

    # AgentProcess Table
    cursor.execute("""
        CREATE TABLE AgentProcess (
            Process_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            User_ID INTEGER,
            Agent_Name TEXT,
            Agent_Priming TEXT DEFAULT NULL,
            AI_Model TEXT,
            Operation_Selected INTEGER,
            Created_At DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (Operation_Selected) REFERENCES TaskDef(TaskDef_ID)
        );
    """)

    # Seed TaskDefs
    cursor.executemany("""
        INSERT INTO TaskDef (TaskDef_Name, TaskDef_Description)
        VALUES (?, ?)
    """, [
        ("summarise", "Summarise any document or text file."),
        ("sentiment_analysis", "Detect sentiment from text.")
    ])

    # Get IDs
    cursor.execute("SELECT TaskDef_ID FROM TaskDef WHERE TaskDef_Name='summarise'")
    summarise_id = cursor.fetchone()[0]

    cursor.execute("SELECT TaskDef_ID FROM TaskDef WHERE TaskDef_Name='sentiment_analysis'")
    sentiment_id = cursor.fetchone()[0]

    # Seed Stages
    cursor.executemany("""
        INSERT INTO TaskStageDef (TaskDef_ID_FK, TaskStageDef_Type, TaskStageDef_Description)
        VALUES (?, ?, ?)
    """, [
        # Summarise
        (summarise_id, "input", "Receive files for summarisation."),
        (summarise_id, "extract", "Extract key information."),
        (summarise_id, "output", "Display summary."),

        # Sentiment
        (sentiment_id, "input", "Receive text for sentiment analysis."),
        (sentiment_id, "sentiment_extract", "Analyse emotional tone."),
        (sentiment_id, "sentiment_output", "Display sentiment result."),
    ])

    conn.commit()
    conn.close()
    print("Rainn DB initialised (Iteration 3, AgentProcess schema).")


if __name__ == "__main__":
    init_db()
