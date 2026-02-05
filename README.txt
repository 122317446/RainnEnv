README.txt
-----------
Project: Rainn – Guided AI Agent Builder
Student: Karl Concha (122317446)
Supervisor: Mr. Bill Emerson
Iteration: 4 (February 2026)

Purpose:
This README documents the origin of all code used in Iteration 4 of the Rainn
project and confirms compliance with UCC Final Year Project guidelines on
third-party code usage, licensing, and AI assistance.

Iteration 4 focuses on reusable flow exchange (import/export), updated
flow management UX, and continued emphasis on traceable, multi-stage
agent execution.


------------------------------------------------------------
CODE ORIGIN SUMMARY
------------------------------------------------------------

Own Code – 30%

• Design and implementation of reusable flow exchange:
  - Flow export payload schema (rainn.flow.v1)
  - Flow import validation and safe process creation

• UI/UX improvements to flow management:
  - Import flow integrated into “My Flows”
  - Per-flow export action in the list
  - Navigation label updates for clarity

• New helper services:
  - SVG chart rendering for stage artifacts

• Cleanup of legacy and unused components:
  - Removed legacy TaskDef CRUD routes and templates
  - Removed unused TaskDefPrimer model
  - Retired standalone flow import template

• Full understanding, review, and integration of all changes prior to submission.


ChatGPT / AI Assistance – 60%

• Guidance on Iteration 4 flow exchange design:
  - Import/export payload structure
  - Validation strategy and error handling
  - Integration with existing DAO/Service layers

• Assistance with UI integration:
  - Placement of Import/Export controls
  - Feedback messaging and redirect flow
  - Consistent label updates across templates

• Guidance on academic-safe AI attribution:
  - Per-file ChatGPT disclosure headers
  - Appropriate scope of AI acknowledgment
  - README disclosure compliance

• Prompts used (examples):
  - “What’s a clean JSON schema for exporting agent flows?”
  - “How should flow import validation be structured?”
  - “Where should Import/Export live in the UI?”
  - “How can flow management labels be clarified?”
  - “Stage validation implementation”
  - “Best way to add a chart or visualisations for Rainn”
  - “Output format inconsistency”
  - “Instruction conflicting with primer”

All AI-assisted code was reviewed, modified where necessary, fully understood,
and integrated by the student.


UI Framework / External Libraries – 10%

• Tabler UI (Bootstrap-based admin dashboard framework)
  - Used for layout, styling, and UI components
  - Integrated into Flask/Jinja templates
  - No modification of Tabler source code

• Matplotlib
  - Used to render chart artifacts as SVG

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

• Iteration 4 adds reusable flow import/export and updates flow management UI.


------------------------------------------------------------
CONFIRMATION
------------------------------------------------------------

I confirm that:
• All third-party and AI-assisted code has been clearly disclosed above.
• I understand the purpose and behaviour of every file included in this submission.
• The submitted work complies with UCC Final Year Project guidelines.

Signed: Karl Concha
Date: February 2026
