class PromptCompiler:

    def compile_master_prompt(agent_priming, taskdef, stage_defs, input_text):


        agent_priming = agent_priming
        input_text = input_text

        plan_lines = []
        for i, stage in enumerate(stage_defs or []):
            stage_type = getattr(stage, "TaskStageDef_Type", "")
            stage_desc = getattr(stage, "TaskStageDef_Description", "")
            plan_lines.append(f"{i+1}. {stage_type} - {stage_desc}".strip())

        stage_plan = "\n".join(plan_lines).strip()
        if not stage_plan:
            stage_plan = "No stages defined"

        agent_name = getattr(taskdef, "TaskDef_Name", "[Unnamed Agent]")
        agent_desc = getattr(taskdef, "TaskDef_Description", "")

        master_prompt = f""" 
        
        [SYSTEM / PRIMING]
        {agent_priming}

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