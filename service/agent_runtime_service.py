# ==========================================
# File: agent_runtime.py
# Created in iteration: 2
# Author: Karl Concha
#
# ChatGPT (OpenAI, 2025) – Assisted in renaming and
# refactoring the runtime routing structure to align
# with the agent workflow design and FYP Bible
# requirements on code clarity and maintainability.
# Conversation Topic: "Iteration 2 – Agent runtime
# routing and operation dispatch refinement."
# Date of assistance: November 2025
#
# References:
# - None (runtime logic developed manually; only
#   ChatGPT assistance noted above)
# ==========================================

import os

from task_logic.summarise import run_summarise
from task_logic.sentiment import run_sentiment
from task_logic.file_reader import FileReader

from service.task_instance_service import TaskInstanceService
from service.task_stage_instance_service import TaskStageInstanceService
from service.agent_process_service import AgentProcessService
from service.task_def_service import TaskDefService
from service.task_stage_def_service import TaskStageService
from service.prompt_complier import PromptCompiler



class AgentRuntime:
    """
    The runtime engine responsible for executing the agent's operations.
    Now supports Iteration 3 Stage 0:
    - Input normalisation to plain text
    - Writing initial artifact (00_input_original.txt)
    - Creating TaskInstance + TaskStageInstance execution records
    """

    @staticmethod
    def run_task(process_id, taskdef_id, file_path, original_filename):
        """
        Executes Stage 0 (Input Normalisation) and then routes to the correct task logic
        based on TaskDef_ID.

        Stage 0:
        - Create TaskInstance (RUNNING)
        - Create run folder runs/<TaskInstance_ID>/
        - Create TaskStageInstance (stage order = 0, RUNNING)
        - Read + normalise file into plain text
        - Write 00_input_original.txt
        - Mark Stage 0 COMPLETED and store artifact path
        - Dispatch summarise/sentiment using the artifact path
        """

        task_instance_service = TaskInstanceService()
        task_stage_instance_service = TaskStageInstanceService()

        task_instance_id = None
        stage0_id = None

        try:
            print("Loaded AgentRuntime from:", __file__)
            print("run_task called:", process_id, taskdef_id, original_filename)

            # ------------------------------------------
            # 1) Create TaskInstance (RUNNING)
            # ------------------------------------------
            task_instance_id = task_instance_service.create_task_instance(
                process_id_fk=process_id,
                taskdef_id_fk=taskdef_id,
                status="RUNNING",
                run_folder=""
            )

            # ------------------------------------------
            # 2) Create run folder runs/<TaskInstance_ID>/
            # ------------------------------------------
            run_folder = os.path.join("agent_runs", str(task_instance_id))
            os.makedirs(run_folder, exist_ok=True)
            task_instance_service.update_run_folder(task_instance_id, run_folder)

            # ------------------------------------------
            # 3) Create Stage 0 TaskStageInstance (RUNNING)
            # ------------------------------------------
            stage0_id = task_stage_instance_service.create_stage_instance(
                task_instance_id_fk=task_instance_id,
                stage_order=0,
                stage_name="input_normalisation",
                status="RUNNING",
                output_artifact_path=None
            )

            # ------------------------------------------
            # 4) Read file to plain text (normalisation)
            #    Uses existing FileReader utility
            # ------------------------------------------
            plain_text = FileReader.read_file(file_path)

            # Minimal normalisation pass (consistent newlines)
            if plain_text is None:
                raise Exception("FileReader returned no content.")

            plain_text = plain_text.replace("\r\n", "\n").replace("\r", "\n").strip()

            if plain_text.strip() == "[Unsupported file type]":
                raise Exception(f"Unsupported file type: {original_filename}")

            if len(plain_text) == 0:
                raise Exception("No text content extracted from file.")

            # ------------------------------------------
            # 5) Write initial artifact 00_input_original.txt
            # ------------------------------------------
            artifact_path = os.path.join(run_folder, "00_input_original.txt")
            with open(artifact_path, "w", encoding="utf-8") as f:
                f.write(plain_text)

            # ------------------------------------------
            # 6) Mark Stage 0 COMPLETED (store artifact path)
            # ------------------------------------------
            task_stage_instance_service.mark_stage_completed(stage0_id, artifact_path)

            # ------------------------------------------
            # 7) Compile + Prompt write
            # ------------------------------------------
            process_service = AgentProcessService()
            taskdef_service = TaskDefService()
            stage_service = TaskStageService()

            process = process_service.get_process(process_id)
            taskdef = taskdef_service.get_taskdef_by_id(taskdef_id)
            stage_defs = stage_service.get_stages_for_task(taskdef_id)

            agent_priming = process.Agent_Priming if process else ""

            master_prompt = PromptCompiler.compile_master_prompt(
                agent_priming=agent_priming,
                taskdef=taskdef,
                stage_defs=stage_defs,
                input_text=plain_text
            )

            master_prompt_path = os.path.join(run_folder, "00_master_prompt.txt")
            with open(master_prompt_path, "w", encoding="utf-8") as f:
                f.write(master_prompt)


            # ------------------------------------------
            # 8) Dispatch task logic using normalised artifact
            # ------------------------------------------
            if taskdef_id == 1:
                output = run_summarise(artifact_path)

            elif taskdef_id == 2:
                output = run_sentiment(artifact_path)

            else:
                output = "[Unsupported Task]"

            # ------------------------------------------
            # 8) Mark TaskInstance as COMPLETED (for now)
            # ------------------------------------------
            task_instance_service.update_status(task_instance_id, "COMPLETED")

            return output

        except Exception as e:
            # Mark stage failed if stage row exists
            if stage0_id is not None:
                try:
                    task_stage_instance_service.mark_stage_failed(stage0_id, str(e))
                except Exception:
                    pass

            # Mark task failed if task row exists
            if task_instance_id is not None:
                try:
                    task_instance_service.update_status(task_instance_id, "FAILED")
                except Exception:
                    pass

            return f"Error: {e}"
