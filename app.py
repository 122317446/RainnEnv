# ==========================================
# File: app.py
# Updated in iteration: 2
# Author: Karl Concha
#
# #ChatGPT (OpenAI, 2025) – Assisted in refactoring Flask routing
# to use modular DAO + Service layers following supervisor
# feedback. Updated naming (Pipeline → Process) to match
# revised architecture and ERD in Iteration 2.
#
# Conversation Topic: "Rainn Iteration 2 – Modular Routing + Process Runner"
# ==========================================

from flask import Flask, render_template, request, redirect, url_for

# ==========================================
# SERVICE IMPORTS
# ==========================================
from service.task_def_service import TaskDefService
from service.task_stage_def_service import TaskStageService
from service.agent_process_service import AgentProcessService
from service.agent_runtime import AgentRuntime

import tempfile, os


# ==========================================
# INITIALISE APP + SERVICES
# ==========================================
app = Flask(__name__)

taskdef_service = TaskDefService()
stage_service = TaskStageService()
process_service = AgentProcessService()
agent_runtime = AgentRuntime()


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
    """
    return render_template(
        "database_view.html",
        taskdefs=taskdef_service.list_taskdefs(),
        taskstages=stage_service.list_all_stages(),
        processes=process_service.list_processes()
    )

@app.route("/test_agent")
def test_agent_page():
    """
    Shows the Agent Processes available in a page
    """
    return render_template(
        "agent_test_list.html",
        processes=process_service.list_processes()
    )

# ==========================================
# CREATE TASKDEF (Agent Template)
# ==========================================
@app.route("/add_agent", methods=["GET", "POST"])
def add_agent():

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

    stage = stage_service.taskstage_dao.get_TaskStageDef_by_id(stage_id)

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
    stage_service.delete_stages_for_task(taskdef_id)
    taskdef_service.delete_taskdef(taskdef_id)
    return redirect(url_for("home_page"))


# ==========================================
# AGENT BUILDER (AgentProcess Creator)
# ==========================================
@app.route("/agent_builder", methods=["GET", "POST"])
def agent_builder_page():

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

    if request.method == "POST":
        agent_name = request.form.get("agent_name")
        ai_model = request.form.get("ai_model")

        new_process = process_service.create_process(
            user_id=1,
            agent_name=agent_name,
            taskdef_id=selected_taskdef,
            ai_model=ai_model
        )

        agent_created = True
        saved_process_id = new_process.Process_ID

    return render_template(
        "agent_builder.html",
        taskdefs=taskdefs,
        stages=stages,
        selected_taskdef=selected_taskdef,
        agent_saved=agent_created,
        saved_process_id=saved_process_id
    )


# ==========================================
# AGENT RUNTIME — RUN PROCESS
# ==========================================
@app.route("/agent_runner/<int:process_id>", methods=["GET", "POST"])
def agent_runner_page(process_id):

    process = process_service.get_process(process_id)
    if not process:
        return "Agent Process not found.", 404

    taskdef = taskdef_service.get_taskdef_by_id(process.Operation_Selected)
    stages = stage_service.get_stages_for_task(taskdef.TaskDef_ID)

    file_text = None

    if request.method == "POST":
        uploaded = request.files.get("uploaded_file")

        if not uploaded:
            file_text = "No file uploaded"
        else:
            ext = os.path.splitext(uploaded.filename)[1]

            with tempfile.NamedTemporaryFile(delete=True, suffix=ext) as tmp:
                tmp.write(uploaded.read())
                tmp.flush()

                try:
                    file_text = agent_runtime.run_task(
                        taskdef_id=taskdef.TaskDef_ID,
                        file_path=tmp.name
                    )
                except Exception as e:
                    file_text = f"Error: {e}"

    return render_template(
        "process_viewer.html",
        process=process,
        taskdef=taskdef,
        stages=stages,
        file_text=file_text
    )


# ==========================================
# UPDATE AGENT PROCESS
# ==========================================
@app.route("/update_process/<int:process_id>", methods=["GET", "POST"])
def update_process(process_id):

    process = process_service.get_process(process_id)
    if not process:
        return "Agent Process not found.", 404

    all_taskdefs = taskdef_service.list_taskdefs()

    if request.method == "POST":
        process.Agent_Name = request.form.get("agent_name")
        process.Operation_Selected = int(request.form.get("operation_selected"))

        process_service.update_process(process)
        return redirect(url_for("database_page"))

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
    process_service.delete_process(process_id)
    return redirect(url_for("database_page"))


# ==========================================
# RUN APP
# ==========================================
if __name__ == "__main__":
    app.run(debug=True)
