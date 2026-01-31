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
        (
            "invoice_compliance",
            "Check invoices for missing fields, inconsistencies, and payment risks across supplier formats."
        ),
        (
            "workload_analysis",
            "Summarise workload distribution and deadline risk across multiple documents."
        )
    ])

    # Fetch IDs for seeded TaskDefs
    cursor.execute("SELECT TaskDef_ID FROM TaskDef WHERE TaskDef_Name='invoice_compliance'")
    invoice_id = cursor.fetchone()[0]

    cursor.execute("SELECT TaskDef_ID FROM TaskDef WHERE TaskDef_Name='workload_analysis'")
    workload_id = cursor.fetchone()[0]

    # Seed Stages
    cursor.executemany("""
        INSERT INTO TaskStageDef (TaskDef_ID_FK, TaskStageDef_Type, TaskStageDef_Description)
        VALUES (?, ?, ?)
    """, [
        # Invoice compliance pipeline
        (invoice_id, "input", "Receive invoice files for compliance checks."),
        (invoice_id, "extract", "Extract supplier, invoice number, dates, totals, and line items."),
        (invoice_id, "validate", "Check for missing fields, inconsistent totals, and date/payment issues."),
        (invoice_id, "risk_flags", "List compliance risks or late-payment concerns with short reasons."),
        (invoice_id, "graph", "Visualise key risks and totals as an SVG chart. Output ONLY valid <svg> markup."),
        (invoice_id, "output", "Provide a concise compliance summary and next steps."),

        # Workload analysis pipeline
        (workload_id, "input", "Receive workload documents or summaries."),
        (workload_id, "extract", "Extract tasks, owners, deadlines, and effort estimates."),
        (workload_id, "aggregate", "Group by owner and time window, highlighting bottlenecks."),
        (workload_id, "risk_flags", "Identify deadline risks and overloaded owners."),
        (workload_id, "graph", "Visualise workload distribution as an SVG chart. Output ONLY valid <svg> markup."),
        (workload_id, "output", "Summarise workload balance and risks with recommendations."),
    ])

    # Seed Agent Processes (pre-defined configured agents)
    cursor.executemany("""
        INSERT INTO AgentProcess (User_ID, Agent_Name, Agent_Priming, AI_Model, Operation_Selected)
        VALUES (?, ?, ?, ?, ?)
    """, [
        (
            1,
            "Invoice Compliance Checker",
            "You are a compliance analyst. Be strict, accurate, and concise.",
            "llama3.1:8b",
            invoice_id
        ),
        (
            1,
            "Invoice Risk Visualiser",
            "Surface compliance risks and make them easy to understand at a glance.",
            "gemma3:4b",
            invoice_id
        ),
        (
            1,
            "Workload Risk Scanner",
            "Identify workload imbalance and deadline risk with clear evidence.",
            "llama3.1:8b",
            workload_id
        ),
    ])

    conn.commit()
    conn.close()
    print("Rainn DB initialised (Iteration 3 schema: AgentProcess + Instance traceability).")


if __name__ == "__main__":
    init_db()
