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

    # AgentProcess Table
    cursor.execute("""
        CREATE TABLE AgentProcess (
            Process_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            User_ID INTEGER,
            Agent_Name TEXT,
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
    print("✔ Rainn DB initialised (Iteration 2, AgentProcess schema).")


if __name__ == "__main__":
    init_db()
