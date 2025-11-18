# ==========================================
# File: init_db.py
# Updated in iteration: 2
# Author: Karl Concha
#
# #ChatGPT (OpenAI, 2025) – Assisted in creating a clean, modular database
# schema matching the new TaskDef, TaskStageDef and AgentPipeline structure.
# Conversation Topic: "Rainn Iteration 2 – Reinitialising schema"
# Date: November 2025
# ==========================================

import sqlite3

def init_db():
    conn = sqlite3.connect("rainn.db")
    cursor = conn.cursor()

    # --------------------------------------
    # DROP existing tables for clean reset
    # --------------------------------------
    cursor.execute("DROP TABLE IF EXISTS TaskStageDef")
    cursor.execute("DROP TABLE IF EXISTS TaskDef")
    cursor.execute("DROP TABLE IF EXISTS AgentPipeline")

    # --------------------------------------
    # TaskDef (operation types)
    # --------------------------------------
    cursor.execute("""
        CREATE TABLE TaskDef (
            TaskDef_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            TaskDef_Name TEXT NOT NULL UNIQUE,
            TaskDef_Description TEXT
        );
    """)

    # --------------------------------------
    # TaskStageDef (pipeline stages)
    # --------------------------------------
    cursor.execute("""
        CREATE TABLE TaskStageDef (
            TaskStageDef_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            TaskDef_ID_FK INTEGER,
            TaskStageDef_Type TEXT,
            TaskStageDef_Description TEXT,
            FOREIGN KEY (TaskDef_ID_FK) REFERENCES TaskDef(TaskDef_ID)
        );
    """)

    # --------------------------------------
    # AgentPipeline (user-created agents)
    # --------------------------------------
    cursor.execute("""
        CREATE TABLE AgentPipeline (
            Input_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            User_ID INTEGER,
            Agent_Name TEXT,
            Text_Input TEXT,
            File_Text TEXT,
            Operation_Selected INTEGER,
            Directory_Path TEXT,
            Created_At DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (Operation_Selected) REFERENCES TaskDef(TaskDef_ID)
        );
    """)

    # --------------------------------------
    # Seed TaskDefs (ONLY 2 for Iteration 2)
    # --------------------------------------
    cursor.executemany("""
        INSERT INTO TaskDef (TaskDef_Name, TaskDef_Description)
        VALUES (?, ?)
    """, [
        ("summarise", "Summarise any document or text file."),
        ("sentiment_analysis", "Detect sentiment from text (positive/neutral/negative).")
    ])

    # Retrieve IDs
    cursor.execute("SELECT TaskDef_ID FROM TaskDef WHERE TaskDef_Name='summarise'")
    summarise_id = cursor.fetchone()[0]

    cursor.execute("SELECT TaskDef_ID FROM TaskDef WHERE TaskDef_Name='sentiment_analysis'")
    sentiment_id = cursor.fetchone()[0]

    # --------------------------------------
    # Seed TaskStageDefs (simple, static)
    # --------------------------------------
    cursor.executemany("""
        INSERT INTO TaskStageDef (TaskDef_ID_FK, TaskStageDef_Type, TaskStageDef_Description)
        VALUES (?, ?, ?)
    """, [
        (summarise_id, "summarise", "Extract and summarise text."),
        (sentiment_id, "sentiment", "Run sentiment analysis on text.")
    ])

    conn.commit()
    conn.close()
    print("✔ Rainn database initialised successfully (Iteration 2 schema).")

if __name__ == "__main__":
    init_db()
