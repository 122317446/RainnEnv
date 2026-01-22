# ==========================================
# File: init_db.py
# Updated in iteration: 3
# Author: Karl Concha
#
# Purpose:
# Initialises the Rainn SQLite database schema.
# Iteration 3 updates introduce execution traceability tables:
# - TaskInstance (one per agent run)
# - TaskStageInstance (one per stage execution within a run)
#
# #ChatGPT (OpenAI, 2025) – Assisted in validating the Iteration 3 schema
# updates by correcting foreign key targets, drop/create ordering, and
# ensuring the TaskInstance/TaskStageInstance tables support artifact
# traceability and stop-on-failure runtime behaviour.
# Conversation Topic: "DB Schema for TaskInstance and TaskStageInstance"
# Date: January 2026
# ==========================================

import sqlite3


def init_db():
    conn = sqlite3.connect("rainn.db")
    cursor = conn.cursor()

    # Recommended for SQLite: enforce FK constraints (OFF by default in SQLite).
    cursor.execute("PRAGMA foreign_keys = ON;")

    # ------------------------------------------
    # DROP OLD TABLES
    # Drop children first (tables with foreign keys) to avoid FK drop errors.
    # ------------------------------------------
    cursor.execute("DROP TABLE IF EXISTS TaskStageInstance;")
    cursor.execute("DROP TABLE IF EXISTS TaskInstance;")
    cursor.execute("DROP TABLE IF EXISTS TaskStageDef;")
    cursor.execute("DROP TABLE IF EXISTS AgentProcess;")
    cursor.execute("DROP TABLE IF EXISTS TaskDef;")

    # ------------------------------------------
    # CORE TEMPLATE TABLES (Iteration 1/2)
    # ------------------------------------------

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
            TaskDef_ID_FK INTEGER NOT NULL,
            TaskStageDef_Type TEXT NOT NULL,
            TaskStageDef_Description TEXT,
            FOREIGN KEY (TaskDef_ID_FK) REFERENCES TaskDef(TaskDef_ID)
        );
    """)

    # AgentProcess Table (Iteration 2)
    # Represents a saved "configured agent" with model + priming + selected template.
    cursor.execute("""
        CREATE TABLE AgentProcess (
            Process_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            User_ID INTEGER,
            Agent_Name TEXT,
            Agent_Priming TEXT DEFAULT NULL,
            AI_Model TEXT,
            Operation_Selected INTEGER NOT NULL,
            Created_At DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (Operation_Selected) REFERENCES TaskDef(TaskDef_ID)
        );
    """)

    # ------------------------------------------
    # EXECUTION TRACEABILITY TABLES (Iteration 3)
    # ------------------------------------------

    # TaskInstance Table (NEW Iteration 3)
    # One row per execution run:
    # "User ran AgentProcess Y using TaskDef Z at time T"
    cursor.execute("""
        CREATE TABLE TaskInstance (
            TaskInstance_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Process_ID_FK INTEGER NOT NULL,
            TaskDef_ID_FK INTEGER NOT NULL,
            Status TEXT CHECK(Status IN ('RUNNING', 'COMPLETED', 'FAILED')) NOT NULL,
            Run_Folder TEXT NOT NULL DEFAULT '',
            Created_At DATETIME DEFAULT CURRENT_TIMESTAMP,
            Updated_At DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (Process_ID_FK) REFERENCES AgentProcess(Process_ID),
            FOREIGN KEY (TaskDef_ID_FK) REFERENCES TaskDef(TaskDef_ID)
        );
    """)

    # TaskStageInstance Table (NEW Iteration 3)
    # One row per stage execution within a TaskInstance.
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

    # ------------------------------------------
    # SEED DATA (DEV / DEMO)
    # ------------------------------------------
    cursor.executemany("""
        INSERT INTO TaskDef (TaskDef_Name, TaskDef_Description)
        VALUES (?, ?)
    """, [
        ("summarise", "Summarise any document or text file."),
        ("sentiment_analysis", "Detect sentiment from text.")
    ])

    # Fetch IDs for seeded TaskDefs
    cursor.execute("SELECT TaskDef_ID FROM TaskDef WHERE TaskDef_Name='summarise'")
    summarise_id = cursor.fetchone()[0]

    cursor.execute("SELECT TaskDef_ID FROM TaskDef WHERE TaskDef_Name='sentiment_analysis'")
    sentiment_id = cursor.fetchone()[0]

    # Seed Stages
    cursor.executemany("""
        INSERT INTO TaskStageDef (TaskDef_ID_FK, TaskStageDef_Type, TaskStageDef_Description)
        VALUES (?, ?, ?)
    """, [
        # Summarise pipeline
        (summarise_id, "input", "Receive files for summarisation."),
        (summarise_id, "extract", "Extract key information."),
        (summarise_id, "output", "Display summary."),

        # Sentiment pipeline
        (sentiment_id, "input", "Receive text for sentiment analysis."),
        (sentiment_id, "sentiment_extract", "Analyse emotional tone."),
        (sentiment_id, "sentiment_output", "Display sentiment result."),
    ])

    conn.commit()
    conn.close()
    print("Rainn DB initialised (Iteration 3 schema: AgentProcess + Instance traceability).")


if __name__ == "__main__":
    init_db()
