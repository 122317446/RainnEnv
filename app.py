# ==========================================
# File: app.py
# Updated in iteration: 3
# Author: Karl Concha
#
# Purpose:
# Flask entrypoint for Rainn (Guided AI Agent Builder).
#
# Iteration 3 Notes:
# - Runtime execution now creates TaskInstance + TaskStageInstance records
# - Uploaded files are normalised to text (Stage 0) and written to artifacts
# - DB view now includes TaskInstance and TaskStageInstance listings
#
# #ChatGPT (OpenAI, 2025) – Assisted in refactoring Flask routing
# to use modular DAO + Service layers following supervisor
# feedback. Updated naming (Pipeline → Process) to match
# revised architecture and ERD in Iteration 2.
# Conversation Topic: "Rainn Iteration 2 – Modular Routing + Process Runner"
# Date: January 2026
# ==========================================

from flask import Flask, render_template, request, redirect, url_for, send_file, abort
import tempfile
import os

# ==========================================
# SERVICE IMPORTS
# ==========================================
from service.task_def_service import TaskDefService
from service.task_stage_def_service import TaskStageService
from service.agent_process_service import AgentProcessService
from service.agent_runtime_service import AgentRuntime
from service.task_instance_service import TaskInstanceService
from service.task_stage_instance_service import TaskStageInstanceService


# ==========================================
# INITIALISE APP + SERVICES
# ==========================================
app = Flask(__name__)

taskdef_service = TaskDefService()
stage_service = TaskStageService()
process_service = AgentProcessService()
agent_runtime = AgentRuntime()

# Iteration 3: instance tracking services (execution traceability)
task_instance = TaskInstanceService()
task_stage_instance = TaskStageInstanceService()


# ==========================================
# HOME / INDEX
# ==========================================
@app.route("/")
def home_page():
    """
    Displays all TaskDefs and their TaskStageDefs.
    Stages grouped by TaskDef_ID for clarity.
    """
    taskdefs = taskdef_service.list_taskdefs()
    stages = stage_service.list_all_stages()

    stages_by_agent = {}
    for st in stages:
        stages_by_agent.setdefault(st.TaskDef_ID_FK, []).append(st)

    return render_template(
        "index.html",
        taskdefs=taskdefs,
        stages_by_agent=stages_by_agent
    )


# ==========================================
# DATABASE VIEW (Debugging) + Agent Process List
# ==========================================
@app.route("/DbView")
def database_page():
    """
    Shows TaskDefs, TaskStages, and AgentProcesses for debugging.
    Iteration 3: Shows TaskInstances and TaskStageInstances.
    """
    return render_template(
        "database_view.html",
        taskdefs=taskdef_service.list_taskdefs(),
        taskstages=stage_service.list_all_stages(),
        processes=process_service.list_processes(),
        task_instances=task_instance.list_task_instances(),
        task_stage_instances=task_stage_instance.list_stage_instances()
    )


# ==========================================
# PROCESS LIST (Agent Test Page)
# ==========================================
@app.route("/test_agent")
def test_agent_page():
    """
    Shows the Agent Processes available in a page.
    """
    taskdefs = taskdef_service.list_taskdefs()
    taskdef_map = {t.TaskDef_ID: t for t in taskdefs}
    return render_template(
        "agent_test_list.html",
        processes=process_service.list_processes(),
        taskdef_map=taskdef_map
    )


# ==========================================
# CREATE TASKDEF (Agent Template)
# ==========================================
@app.route("/add_agent", methods=["GET", "POST"])
def add_agent():
    """
    Creates a TaskDef (agent template) plus its stage definitions.
    """
    if request.method == "POST":
        name = request.form.get("agent_name")
        desc = request.form.get("agent_description")

        # Create TaskDef
        new_taskdef_id = taskdef_service.create_taskdef(name, desc)

        # Create attached stages
        stage_names = request.form.getlist("stage_name[]")
        stage_descs = request.form.getlist("stage_desc[]")

        for s_name, s_desc in zip(stage_names, stage_descs):
            stage_service.create_stage(new_taskdef_id, s_name, s_desc)

        return redirect(url_for("home_page"))

    return render_template("add_agent.html")


# ==========================================
# UPDATE TASKDEF
# ==========================================
@app.route("/update_agent/<int:taskdef_id>", methods=["GET", "POST"])
def update_agent(taskdef_id):
    """
    Updates an existing TaskDef and displays its stages.
    """
    agent = taskdef_service.get_taskdef_by_id(taskdef_id)
    agent_stages = stage_service.get_stages_for_task(taskdef_id)

    if request.method == "POST":
        updated_name = request.form.get("agent_name")
        updated_desc = request.form.get("agent_description")

        taskdef_service.update_taskdef(taskdef_id, updated_name, updated_desc)
        return redirect(url_for("home_page"))

    return render_template("update_agent.html", agent=agent, stages=agent_stages)


# ==========================================
# UPDATE A STAGE
# ==========================================
@app.route("/update_stage/<int:stage_id>", methods=["GET", "POST"])
def update_stage(stage_id):
    """
    Updates an existing TaskStageDef.
    """
    stage = stage_service.get_stage_by_id(stage_id)
    if not stage:
        return "Stage not found.", 404

    if request.method == "POST":
        updated_stage = stage.__class__(
            stage.TaskStageDef_ID,
            stage.TaskDef_ID_FK,
            request.form.get("stage_type"),
            request.form.get("stage_desc")
        )
        stage_service.taskstage_dao.update_TaskStageDef(updated_stage)

        return redirect(url_for("update_agent", taskdef_id=stage.TaskDef_ID_FK))

    return render_template("update_stage.html", stage=stage)


# ==========================================
# DELETE AGENT (TaskDef + Stages)
# ==========================================
@app.route("/delete_agent/<int:taskdef_id>", methods=["POST"])
def delete_agent(taskdef_id):
    """
    Deletes a TaskDef and all stages attached to it.
    """
    stage_service.delete_stages_for_task(taskdef_id)
    taskdef_service.delete_taskdef(taskdef_id)
    return redirect(url_for("home_page"))


# ==========================================
# AGENT BUILDER (AgentProcess Creator)
# ==========================================
@app.route("/agent_builder", methods=["GET", "POST"])
def agent_builder_page():
    """
    Creates an AgentProcess (configured runnable agent).
    Uses the working zip-style create_process signature.
    """
    taskdefs = taskdef_service.list_taskdefs()

    selected_taskdef = (
        request.args.get("operation_selected") or
        request.form.get("operation_selected")
    )

    stages = None
    if selected_taskdef:
        selected_taskdef = int(selected_taskdef)
        stages = stage_service.get_stages_for_task(selected_taskdef)

    agent_created = False
    saved_process_id = None
    edit_stages = []
    error_message = None
    step = "details"
    agent_name_val = request.form.get("agent_name") if request.method == "POST" else ""
    agent_priming_val = request.form.get("agent_priming") if request.method == "POST" else ""
    ai_model_val = request.form.get("ai_model") if request.method == "POST" else ""
    from_scratch_val = request.form.get("from_scratch") == "on" if request.method == "POST" else False

    def _normalize_stages(stage_names, stage_descs):
        normalized = []
        for s_name, s_desc in zip(stage_names, stage_descs):
            stage_type = (s_name or "").strip()
            stage_desc = (s_desc or "").strip()
            if not stage_type and not stage_desc:
                continue
            if stage_type.lower() == "input":
                continue
            normalized.append((stage_type, stage_desc))
        if not normalized or normalized[-1][0].lower() != "output":
            normalized.append(("output", "Present the final response for the user."))
        return normalized

    if request.method == "POST":
        action = request.form.get("action") or "save"
        from_scratch = request.form.get("from_scratch") == "on"

        if action == "next":
            step = "template"
            return render_template(
                "agent_builder.html",
                taskdefs=taskdefs,
                stages=stages,
                selected_taskdef=selected_taskdef,
                agent_saved=agent_created,
                saved_process_id=saved_process_id,
                step=step,
                edit_stages=[],
                from_scratch=from_scratch,
                agent_name=agent_name_val,
                agent_priming=agent_priming_val,
                ai_model=ai_model_val
            )

        if action == "back_details":
            step = "details"
            return render_template(
                "agent_builder.html",
                taskdefs=taskdefs,
                stages=stages,
                selected_taskdef=selected_taskdef,
                agent_saved=agent_created,
                saved_process_id=saved_process_id,
                step=step,
                edit_stages=[],
                from_scratch=from_scratch,
                agent_name=agent_name_val,
                agent_priming=agent_priming_val,
                ai_model=ai_model_val
            )

        if action == "choose_template":
            step = "stages"
            if not from_scratch and not selected_taskdef:
                error_message = "Choose a template or start from scratch."
                return render_template(
                    "agent_builder.html",
                    taskdefs=taskdefs,
                    stages=stages,
                    selected_taskdef=selected_taskdef,
                    agent_saved=agent_created,
                    saved_process_id=saved_process_id,
                    step="template",
                    edit_stages=[],
                    from_scratch=from_scratch,
                    agent_name=agent_name_val,
                    agent_priming=agent_priming_val,
                    ai_model=ai_model_val,
                    error_message=error_message
                )
            if from_scratch:
                edit_stages = [
                    ("extract", "Extract the key points."),
                    ("output", "Present the final response for the user.")
                ]
            else:
                edit_stages = [
                (s.TaskStageDef_Type, s.TaskStageDef_Description)
                for s in stage_service.get_stages_for_task(selected_taskdef)
                if (getattr(s, "TaskStageDef_Type", "") or "").strip().lower() != "input"
            ]
            return render_template(
                "agent_builder.html",
                taskdefs=taskdefs,
                stages=stages,
                preview_stages=edit_stages,
                selected_taskdef=selected_taskdef,
                agent_saved=agent_created,
                saved_process_id=saved_process_id,
                step=step,
                edit_stages=edit_stages,
                from_scratch=from_scratch,
                agent_name=agent_name_val,
                agent_priming=agent_priming_val,
                ai_model=ai_model_val
            )

        if action in ("review", "back_template", "back_stages", "save"):
            stage_names = request.form.getlist("stage_name[]")
            stage_descs = request.form.getlist("stage_desc[]")
            has_custom = any(
                (n or "").strip() or (d or "").strip()
                for n, d in zip(stage_names, stage_descs)
            )
            if not from_scratch and selected_taskdef and not has_custom:
                blueprint_stage_objs = [
                    s for s in stage_service.get_stages_for_task(selected_taskdef)
                    if (getattr(s, "TaskStageDef_Type", "") or "").strip().lower() != "input"
                ]
                edit_stages = _normalize_stages(
                    [s.TaskStageDef_Type for s in blueprint_stage_objs],
                    [s.TaskStageDef_Description for s in blueprint_stage_objs]
                )
            else:
                edit_stages = _normalize_stages(stage_names, stage_descs)

        if action == "back_template":
            step = "template"
            return render_template(
                "agent_builder.html",
                taskdefs=taskdefs,
                stages=stages,
                preview_stages=edit_stages,
                selected_taskdef=selected_taskdef,
                agent_saved=agent_created,
                saved_process_id=saved_process_id,
                step=step,
                edit_stages=edit_stages,
                from_scratch=from_scratch,
                agent_name=agent_name_val,
                agent_priming=agent_priming_val,
                ai_model=ai_model_val
            )

        if action == "review":
            if not from_scratch and not selected_taskdef:
                error_message = "Choose a template or start from scratch to continue."
                return render_template(
                    "agent_builder.html",
                    taskdefs=taskdefs,
                    stages=stages,
                    preview_stages=edit_stages,
                    selected_taskdef=selected_taskdef,
                    agent_saved=agent_created,
                    saved_process_id=saved_process_id,
                    step="stages",
                    edit_stages=edit_stages,
                    from_scratch=from_scratch,
                    agent_name=agent_name_val,
                    agent_priming=agent_priming_val,
                    ai_model=ai_model_val,
                    error_message=error_message
                )
            step = "review"
            return render_template(
                "agent_builder.html",
                taskdefs=taskdefs,
                stages=stages,
                preview_stages=edit_stages,
                selected_taskdef=selected_taskdef,
                agent_saved=agent_created,
                saved_process_id=saved_process_id,
                step=step,
                edit_stages=edit_stages,
                from_scratch=from_scratch,
                agent_name=agent_name_val,
                agent_priming=agent_priming_val,
                ai_model=ai_model_val
            )

        if action == "back_stages":
            step = "stages"
            return render_template(
                "agent_builder.html",
                taskdefs=taskdefs,
                stages=stages,
                preview_stages=edit_stages,
                selected_taskdef=selected_taskdef,
                agent_saved=agent_created,
                saved_process_id=saved_process_id,
                step=step,
                edit_stages=edit_stages,
                from_scratch=from_scratch,
                agent_name=agent_name_val,
                agent_priming=agent_priming_val,
                ai_model=ai_model_val
            )

        agent_name = request.form.get("agent_name")
        agent_priming = request.form.get("agent_priming")
        ai_model = request.form.get("ai_model")

        edited_stages = edit_stages or _normalize_stages(
            request.form.getlist("stage_name[]"),
            request.form.getlist("stage_desc[]")
        )

        taskdef_id_to_use = selected_taskdef
        from_scratch = request.form.get("from_scratch") == "on"

        if from_scratch:
            base_name = (agent_name or "Custom Agent").strip()
            candidate_name = f"Custom - {base_name}"
            existing_names = {t.TaskDef_Name for t in taskdefs}
            if candidate_name in existing_names:
                suffix = 1
                while f"{candidate_name} ({suffix})" in existing_names:
                    suffix += 1
                candidate_name = f"{candidate_name} ({suffix})"

            taskdef_id_to_use = taskdef_service.create_taskdef(
                candidate_name,
                "Custom template created by user."
            )
            for s_name, s_desc in edited_stages:
                stage_service.create_stage(taskdef_id_to_use, s_name, s_desc)
        else:
            if not selected_taskdef:
                error_message = "Select a blueprint template or choose 'Start from scratch' to save."
                return render_template(
                    "agent_builder.html",
                    taskdefs=taskdefs,
                    stages=stages,
                    selected_taskdef=selected_taskdef,
                    agent_saved=agent_created,
                    saved_process_id=saved_process_id,
                    step="stages",
                    edit_stages=edit_stages,
                    from_scratch=from_scratch,
                    agent_name=agent_name_val,
                    agent_priming=agent_priming_val,
                    ai_model=ai_model_val,
                    error_message=error_message
                )
            blueprint = []
            if selected_taskdef:
                blueprint_stage_objs = [
                    s for s in stage_service.get_stages_for_task(selected_taskdef)
                    if (getattr(s, "TaskStageDef_Type", "") or "").strip().lower() != "input"
                ]
                blueprint = _normalize_stages(
                    [s.TaskStageDef_Type for s in blueprint_stage_objs],
                    [s.TaskStageDef_Description for s in blueprint_stage_objs]
                )

            if edited_stages != blueprint:
                base_name = (agent_name or "Custom Agent").strip()
                candidate_name = f"Custom - {base_name}"
                existing_names = {t.TaskDef_Name for t in taskdefs}
                if candidate_name in existing_names:
                    suffix = 1
                    while f"{candidate_name} ({suffix})" in existing_names:
                        suffix += 1
                    candidate_name = f"{candidate_name} ({suffix})"

                taskdef_id_to_use = taskdef_service.create_taskdef(
                    candidate_name,
                    "Custom template created by user."
                )
                for s_name, s_desc in edited_stages:
                    stage_service.create_stage(taskdef_id_to_use, s_name, s_desc)

        # IMPORTANT:
        # Keep the zip version signature (it works with your current service).
        new_process = process_service.create_process(
            user_id=1,
            agent_name=agent_name,
            agent_priming=agent_priming,
            taskdef_id=taskdef_id_to_use,
            ai_model=ai_model
        )

        agent_created = True
        saved_process_id = new_process.Process_ID
        step = "review"

    preview_stages = None
    if edit_stages:
        preview_stages = edit_stages
    elif stages:
        preview_stages = [
            (s.TaskStageDef_Type, s.TaskStageDef_Description)
            for s in stages
            if (getattr(s, "TaskStageDef_Type", "") or "").strip().lower() != "input"
        ]

    return render_template(
        "agent_builder.html",
        taskdefs=taskdefs,
        stages=stages,
        preview_stages=preview_stages,
        selected_taskdef=selected_taskdef,
        agent_saved=agent_created,
        saved_process_id=saved_process_id,
        step=step,
        edit_stages=edit_stages,
        from_scratch=from_scratch_val,
        agent_name=agent_name_val if agent_created else agent_name_val,
        agent_priming=agent_priming_val if agent_created else agent_priming_val,
        ai_model=ai_model_val if agent_created else ai_model_val,
        error_message=error_message
    )


# ==========================================
# AGENT RUNTIME — RUN PROCESS (Iteration 3)
# ==========================================
@app.route("/agent_runner/<int:process_id>", methods=["GET", "POST"])
def agent_runner_page(process_id):
    """
    Executes a selected AgentProcess against a user-uploaded file.

    Iteration 3 runtime behaviour:
    - Creates TaskInstance record (RUNNING)
    - Stage 0 normalises input to text and writes 00_input_original.txt
    - Executes stage 1..N sequentially (stop on first failure)
    - Writes per-stage artifacts and persists paths in TaskStageInstance
    - Marks TaskInstance COMPLETED/FAILED accordingly
    """
    process = process_service.get_process(process_id)
    if not process:
        return "Agent Process not found.", 404

    taskdef = taskdef_service.get_taskdef_by_id(process.Operation_Selected)
    stages = stage_service.get_stages_for_task(taskdef.TaskDef_ID)

    file_text = None
    output_type = None
    output_artifact = None
    output_task_instance_id = None
    output_artifact_name = None

    if request.method == "POST":
        uploaded_files = request.files.getlist("uploaded_file")

        if not uploaded_files:
            file_text = "No file uploaded"
        else:
            temp_files = []
            try:
                for uploaded in uploaded_files:
                    if not uploaded or not uploaded.filename:
                        continue
                    ext = os.path.splitext(uploaded.filename)[1]
                    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
                    tmp.write(uploaded.read())
                    tmp.flush()
                    tmp.close()
                    temp_files.append({
                        "path": tmp.name,
                        "name": uploaded.filename
                    })

                if not temp_files:
                    file_text = "No file uploaded"
                else:
                    result = agent_runtime.run_task(
                        process_id=process_id,
                        taskdef_id=taskdef.TaskDef_ID,
                        file_path=temp_files
                    )  # Iteration 3 changes here to accommodate instances
                    if isinstance(result, dict):
                        file_text = result.get("output_text")
                        output_type = result.get("output_type")
                        output_artifact = result.get("output_artifact_path")
                        output_task_instance_id = result.get("task_instance_id")
                        if output_artifact:
                            output_artifact_name = os.path.basename(output_artifact)
                    else:
                        file_text = result
            except Exception as e:
                file_text = f"Error: {e}"
            finally:
                for f in temp_files:
                    try:
                        os.remove(f["path"])
                    except Exception:
                        pass

    return render_template(
        "process_viewer.html",
        process=process,
        taskdef=taskdef,
        stages=stages,
        file_text=file_text,
        output_type=output_type,
        output_artifact=output_artifact,
        output_task_instance_id=output_task_instance_id,
        output_artifact_name=output_artifact_name
    )


# ==========================================
# UPDATE AGENT PROCESS
# ==========================================
@app.route("/update_process/<int:process_id>", methods=["GET", "POST"])
def update_process(process_id):
    """
    Updates an existing AgentProcess.
    Keeps zip-style update_process(process) behaviour (object mutation).
    """
    process = process_service.get_process(process_id)
    if not process:
        return "Agent Process not found.", 404

    all_taskdefs = taskdef_service.list_taskdefs()

    if request.method == "POST":
        process.Agent_Name = request.form.get("agent_name")
        process.Operation_Selected = int(request.form.get("operation_selected"))

        process_service.update_process(process)
        return redirect(url_for("test_agent_page"))

    return render_template(
        "process_update.html",
        process=process,
        taskdefs=all_taskdefs
    )


# ==========================================
# DELETE AGENT PROCESS
# ==========================================
@app.route("/delete_process/<int:process_id>", methods=["POST"])
def delete_process(process_id):
    """
    Deletes an AgentProcess.
    """
    process_service.delete_process(process_id)
    return redirect(url_for("test_agent_page"))


# ==========================================
# ARTIFACT FILE SERVER (Iteration 4 prep)
# ==========================================
@app.route("/artifact/<int:task_instance_id>/<path:filename>")
def artifact_file(task_instance_id, filename):
    """
    Serves artifact files from agent_runs/<id>/artifacts for inline display.
    """
    artifacts_dir = os.path.join("agent_runs", str(task_instance_id), "artifacts")
    base_dir = os.path.abspath(artifacts_dir)
    requested_path = os.path.abspath(os.path.join(artifacts_dir, filename))

    if not requested_path.startswith(base_dir + os.sep):
        abort(404)

    if not os.path.exists(requested_path):
        abort(404)

    if requested_path.lower().endswith(".svg"):
        return send_file(requested_path, mimetype="image/svg+xml")

    return send_file(requested_path)
