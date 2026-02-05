# ==========================================
# File: agent_runtime_service.py
# Updated in iteration: 4
# Author: Karl Concha
#
# Central runtime orchestrator for executing an AgentProcess.
# Iteration 3 responsibilities (traceable execution):
# - Create TaskInstance (RUNNING) as the top-level execution record
# - Create a per-run folder: agent_runs/<TaskInstance_ID>/
# - Stage 0: read uploaded file, normalise to plain text, write 00_input_original.txt
# - Create TaskStageInstance rows for each stage (stage_order = 0..N)
# - Execute stages sequentially (stop on first failure)
# - Write each stage output to an artifact file and persist the output path
# - Mark TaskInstance COMPLETED/FAILED accordingly
#
# #ChatGPT (OpenAI, 2025) – Assisted in refactoring the runtime execution
# architecture to support multi-stage workflows, explicit failure
# propagation, and artifact traceability, in line with Iteration 3
# requirements and FYP Bible guidelines.
# Conversation Topic: "Iteration 3 – Multi-stage Agent Execution Engine"
# Date: January 2026
#
# Notes:
# - DB logic is done via Service/DAO layers (TaskInstanceService, TaskStageInstanceService)
# - Stage execution is delegated to StageExecutionEngine
# ==========================================

import os

from service.flow.input_normaliser import Stage0InputNormaliser
from service.process.stage_execution_engine import StageExecutionEngine

from service.task_instance_service import TaskInstanceService
from service.task_stage_instance_service import TaskStageInstanceService
from service.process.agent_process_service import AgentProcessService
from service.task_def_service import TaskDefService
from service.task_stage_def_service import TaskStageService

from service.flow.prompt_compiler import PromptCompiler
from service.integrations.model_client_ollama import OllamaModelClient


class AgentRuntime:
    """
    Orchestrates a full agent execution from uploaded file -> stage outputs.

    In Iteration 3,
    - execution lifecycle (TaskInstance status)
    - stage lifecycle (TaskStageInstance status)
    - artifact folder structure
    """

    @staticmethod
    def run_task(process_id, taskdef_id, file_path, original_filename=None):
        """
        Executes Stage 0 (Input Normalisation) and then executes stages 1..N.
        """

        task_instance_service = TaskInstanceService()
        task_stage_instance_service = TaskStageInstanceService()

        task_instance_id = None
        stage0_id = None

        try:
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
            # 2) Create per-run folder: agent_runs/<id>/
            # ------------------------------------------
            run_folder = os.path.join("agent_runs", str(task_instance_id))
            os.makedirs(run_folder, exist_ok=True)
            task_instance_service.update_run_folder(task_instance_id, run_folder)

            artifacts_dir = os.path.join(run_folder, "artifacts")
            os.makedirs(artifacts_dir, exist_ok=True)

            # ------------------------------------------
            # 3) Create Stage 0 TaskStageInstance (RUNNING)
            # ------------------------------------------
            stage0_id = task_stage_instance_service.create_stage_instance(
                task_instance_id_fk=task_instance_id,
                stage_order=0,
                stage_name="input",
                status="RUNNING",
                output_artifact_path=None
            )

            # ------------------------------------------
            # 4) Execute Stage 0 (Input Normalisation) / Input stage
            #    Output: 00_input_original.txt
            # ------------------------------------------
            if isinstance(file_path, list):
                files = file_path
                plain_text, stage0_artifact_path = Stage0InputNormaliser.run_multi(
                    files=files,
                    run_folder=run_folder
                )
            else:
                plain_text, stage0_artifact_path = Stage0InputNormaliser.run(
                    file_path=file_path,
                    run_folder=run_folder,
                    original_filename=original_filename
                )

            # ------------------------------------------
            # 5) Mark Stage 0 COMPLETED (store artifact path) (traceback purposes)
            # ------------------------------------------
            task_stage_instance_service.mark_stage_completed(stage0_id, stage0_artifact_path)

            # ------------------------------------------
            # 6) Load process + template + stage definitions
            # ------------------------------------------
            process_service = AgentProcessService()
            taskdef_service = TaskDefService()
            stage_service = TaskStageService()

            process = process_service.get_process(process_id) #The agent process
            taskdef = taskdef_service.get_taskdef_by_id(taskdef_id)
            stage_defs = stage_service.get_stages_for_task(taskdef_id)

            agent_priming = process.Agent_Priming if process else ""
            model_name = process.AI_Model if process else "mock-model"

            # ------------------------------------------
            # 7) Compile and persist the “master prompt”
            #    This is useful for reporting/debugging.
            # ------------------------------------------
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
            # 8) Execute stages 1..N sequentially
            #    Stops on first failure (exception is raised).
            # ------------------------------------------
            model_client = OllamaModelClient()

            final_output_path, final_output_type = StageExecutionEngine.execute(
                task_instance_id=task_instance_id,
                run_folder=run_folder,
                artifacts_dir=artifacts_dir,
                stage_defs=stage_defs,
                master_prompt=master_prompt,
                model_client=model_client,
                model_name=model_name,
                task_stage_instance_service=task_stage_instance_service,
                stage0_artifact_path=stage0_artifact_path,
                system_prompt=agent_priming
            )

            # ------------------------------------------
            # 9) Read final output artifact (if any)
            # ------------------------------------------
            if final_output_path:
                with open(final_output_path, "r", encoding="utf-8") as f:
                    output_text = f.read()
                output_type = final_output_type or "text"
            else:
                # If there are no executable stages (e.g., only input stage), return stage-0 text
                output_text = plain_text
                output_type = "text"
                final_output_path = stage0_artifact_path

            # ------------------------------------------
            # 10) Write output descriptor (type + path) for UI/debugging
            # ------------------------------------------
            output_descriptor = {
                "task_instance_id": task_instance_id,
                "output_type": output_type,
                "output_path": final_output_path
            }
            descriptor_path = os.path.join(run_folder, "output_descriptor.json")
            with open(descriptor_path, "w", encoding="utf-8") as f:
                import json
                json.dump(output_descriptor, f, indent=2)

            task_instance_service.update_status(task_instance_id, "COMPLETED")
            return {
                "task_instance_id": task_instance_id,
                "output_text": output_text,
                "output_type": output_type,
                "output_artifact_path": final_output_path
            }

        except Exception as e:
            # Mark Stage 0 failed if it exists (or if failure happened during stage-0 path)
            if stage0_id is not None:
                try:
                    task_stage_instance_service.mark_stage_failed(stage0_id, str(e))
                except Exception:
                    pass

            # Mark TaskInstance failed if it exists
            if task_instance_id is not None:
                try:
                    task_instance_service.update_status(task_instance_id, "FAILED")
                except Exception:
                    pass

            return {
                "task_instance_id": task_instance_id,
                "output_text": f"Error: {e}",
                "output_type": "text",
                "output_artifact_path": None
            }
