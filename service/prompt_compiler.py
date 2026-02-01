# ==========================================
# File: prompt_compiler.py
# Created in iteration: 3
# Author: Karl Concha
#
# Build a “master prompt” that describes:
# - agent priming (system intent)
# - agent template metadata (name/description)
# - workflow plan (stages)
# - current input (stage-0 plain text)
#
# #ChatGPT (OpenAI, 2025) – Assisted in designing a structured master
# prompt composition strategy combining agent priming, workflow stages,
# and normalised input text to improve consistency across stages.
# Conversation Topic: "Priming the agent for the given task"
# Date: January 2026
#
# Used in agent_runtime_service.py
# ==========================================


class PromptCompiler:
    """Helper for producing the master prompt that is used to guide stage prompts."""

    @staticmethod
    def compile_master_prompt(agent_priming, taskdef, stage_defs, input_text):
        agent_priming = (agent_priming or "").strip()
        input_text = (input_text or "").strip()

        # Build a readable workflow plan for the model.
        # Note: StageExecutionEngine will skip stages where type == "input".
        plain_lines = []
        for i, stage in enumerate(stage_defs or [], start=1):
            stage_type = (getattr(stage, "TaskStageDef_Type", "") or "").strip()
            stage_desc = (getattr(stage, "TaskStageDef_Description", "") or "").strip()

            if stage_type and stage_desc:
                plain_lines.append(f"{i}. {stage_type} - {stage_desc}")
            elif stage_type:
                plain_lines.append(f"{i}. {stage_type}")
            elif stage_desc:
                plain_lines.append(f"{i}. {stage_desc}")
            else:
                plain_lines.append(f"{i}. [Unnamed Stage]")

        stage_plan = "\n".join(plain_lines).strip() or "No stages defined"

        agent_name = (getattr(taskdef, "TaskDef_Name", None) or "[Unnamed Agent]").strip()
        agent_desc = (getattr(taskdef, "TaskDef_Description", None) or "").strip()

        master_prompt = f"""
[AGENT TEMPLATE]
Name: {agent_name}
Description: {agent_desc}

[WORKFLOW PLAN]
{stage_plan}

[INPUT]
{input_text}

[OUTPUT RULES]
- Follow the workflow plan step-by-step.
- Keep outputs clear and structured.
- Do not invent facts not present in the input.
""".strip()

        return master_prompt
