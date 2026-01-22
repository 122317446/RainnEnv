README.txt
-----------
Project: Rainn – Guided AI Agent Builder
Student: Karl Concha (122317446)
Supervisor: Mr. Bill Emerson
Iteration: 3 (January 2026)

Purpose:
This README documents the origin of all code used in Iteration 3 of the Rainn
project and confirms compliance with UCC Final Year Project guidelines on
third-party code usage, licensing, and AI assistance.

Iteration 3 focuses on runtime execution, multi-stage agent workflows,
artifact traceability, and execution state management.


------------------------------------------------------------
CODE ORIGIN SUMMARY
------------------------------------------------------------

Own Code – 20%

• Design and implementation of the Iteration 3 execution architecture:
  - TaskInstance (per-run execution tracking)
  - TaskStageInstance (per-stage execution tracking)

• Implementation of multi-stage agent execution with:
  - Sequential stage execution
  - Per-stage artifact persistence

• Database schema design and implementation for execution traceability:
  - TaskInstance table
  - TaskStageInstance table
  - Correct foreign-key relationships to AgentProcess and TaskDef

• Implementation of:
  - Stage 0 input normalisation pipeline (file → plain text)
  - Artifact folder structure per execution (agent_runs/<id>/)
  - Runtime status updates (RUNNING / COMPLETED / FAILED)

• Removal of legacy task-specific Python logic (e.g. summarise.py,
  sentiment.py) in favour of a unified, data-driven, prompt-based execution
  model.

• Full understanding, review, and integration of all runtime logic prior
  to submission.


ChatGPT / AI Assistance – 60%

• Architectural guidance for Iteration 3 following supervisor feedback:
  - Separation of static configuration (AgentProcess, TaskDef)
    from runtime execution (TaskInstance, TaskStageInstance)
  - Validation of clean architecture boundaries (DAO / Service / Runtime)

• Assistance with:
  - Designing multi-stage execution flow
  - Stop-on-failure runtime logic
  - Artifact traceability strategy
  - Service-layer refactoring for clarity and maintainability

• Validation and correction of database schema:
  - Foreign-key relationships
  - Drop/create ordering
  - Execution lifecycle fields

• Guidance on academic-safe AI attribution:
  - Per-file ChatGPT disclosure headers
  - Appropriate scope of AI acknowledgment
  - README disclosure compliance

• Prompts used (examples):
  - “How should multi-stage agent execution be structured in relation to Rainn's current system?”
  - “How would I go on to connect Ollama localhost to Rainn?”
  - “Would it be more benificical to further chunk agent_runtime_service to increase traceability”
  - “I have found a new Bootstrap UI framework called Tabler and feel this would be a benificical upgrade for Rainn's UI”
  - “Is this file still used or should it be considered legacy?”

All AI-assisted code was reviewed, modified where necessary, fully understood,
and integrated by the student.


UI Framework / External Libraries – 20%

• Tabler UI (Bootstrap-based admin dashboard framework)
  - Used for layout, styling, and UI components
  - Integrated into Flask/Jinja templates
  - No modification of Tabler source code

• Documentation:
  - Indirect reference via Tabler UI documentation
  - Bootstrap utility classes used as provided

Tabler is used strictly for presentation and does not influence core
application logic or runtime execution.


------------------------------------------------------------
NOTES ON USAGE
------------------------------------------------------------

• All code was developed and tested locally on macOS using:
  - Python 3
  - Flask
  - SQLite

• No proprietary or paid software was used.

• ChatGPT was used strictly as a development aid.

• All AI-assisted logic was reviewed, tested, and understood before inclusion.

• Version control was maintained using Git throughout development.

• Iteration 3 intentionally replaces earlier experimental approaches
  (task-specific Python execution) with a scalable, data-driven,
  prompt-based agent execution model.


------------------------------------------------------------
CONFIRMATION
------------------------------------------------------------

I confirm that:
• All third-party and AI-assisted code has been clearly disclosed above.
• I understand the purpose and behaviour of every file included in this submission.
• The submitted work complies with UCC Final Year Project guidelines.

Signed: Karl Concha
Date: January 2026
