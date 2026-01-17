# ==========================================
# File: stage_execution_engine.py
# Created in iteration: 3
# Author: Karl Concha
#
# Purpose:
# Executes stages 1..N (after Stage 0 is done).
# - Skips stage defs with TaskStageDef_Type == "input"
# - Creates TaskStageInstance per stage
# - Builds per-stage prompt (master prompt + stage directive + current input)
# - Calls model client
# - Writes each stage output to an artifact file
# - Returns the final output artifact path
#
# No DB queries happen here; DB updates are done through the passed service.
# ==========================================

import os


class StageExecutionEngine:
    """ Executes workflow stages using a provided model client and artifact chaining. """

    @staticmethod
    def execute(
        task_instance_id,
        run_folder,
        artifacts_dir,
        stage_defs,
        master_prompt,
        model_client,
        model_name,
        task_stage_instance_service,
        stage0_artifact_path
    ):
        """
        Executes stages 1..N (skipping input) and returns final artifact path.

        Returns:
            final_output_path (str) or None
        """

        os.makedirs(artifacts_dir, exist_ok=True)

        # Sort stages deterministically (by TaskStageDef_ID if present)
        sorted_stages = sorted(stage_defs or [], key=lambda s: getattr(s, "TaskStageDef_ID", 0))

        # Filter out "input" stages (Stage 0 already handled that)
        exec_stages = []
        for s in sorted_stages:
            stage_type = (getattr(s, "TaskStageDef_Type", "") or "").strip().lower()
            if stage_type == "input":
                continue
            exec_stages.append(s)

        current_input_path = stage0_artifact_path
        final_output_path = None

        for i, stage in enumerate(exec_stages, start=1):
            stage_type_raw = (getattr(stage, "TaskStageDef_Type", "") or "").strip()
            stage_desc = (getattr(stage, "TaskStageDef_Description", "") or "").strip()

            # Create stage instance row (RUNNING)
            stage_instance_id = task_stage_instance_service.create_stage_instance(
                task_instance_id_fk=task_instance_id,
                stage_order=i,
                stage_name=stage_type_raw,
                status="RUNNING",
                output_artifact_path=None
            )

            try:
                # Read current input from previous artifact
                with open(current_input_path, "r", encoding="utf-8") as f:
                    input_text = f.read()

                # Build stage prompt
                stage_prompt = StageExecutionEngine._build_stage_prompt(
                    master_prompt=master_prompt,
                    stage_type=stage_type_raw,
                    stage_description=stage_desc,
                    input_text=input_text
                )

                # Call model
                output_text = model_client.generate(model_name, stage_prompt)
                if output_text is None:
                    raise Exception("Model client returned no output.")

                # Write output artifact
                safe_stage_type = stage_type_raw.replace(" ", "_").lower() or "stage"
                out_filename = f"{i:02d}_stage_{safe_stage_type}_output.txt"
                out_path = os.path.join(artifacts_dir, out_filename)

                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(output_text)

                # Mark completed + chain
                task_stage_instance_service.mark_stage_completed(stage_instance_id, out_path)
                current_input_path = out_path
                final_output_path = out_path

            except Exception as e:
                # Mark failed then re-raise so runtime can handle task failure
                try:
                    task_stage_instance_service.mark_stage_failed(stage_instance_id, str(e))
                except Exception:
                    pass
                raise

        return final_output_path

    @staticmethod
    def _build_stage_prompt(master_prompt, stage_type, stage_description, input_text):
        master_prompt = (master_prompt or "").strip()
        stage_type = (stage_type or "").strip()
        stage_description = (stage_description or "").strip()
        input_text = (input_text or "").strip()

        return f"""
{master_prompt}

[CURRENT STAGE]
Type: {stage_type}
Goal: {stage_description}

[CURRENT INPUT]
{input_text}

[INSTRUCTIONS]
Perform ONLY this stage. Output must be suitable as input to the next stage.
""".strip()
