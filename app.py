# ==========================================
# File: app.py
# Updated in iteration: 2
# Author: Karl Concha
#
# #ChatGPT (OpenAI, 2025) – Assisted in restructuring Flask routing to
# adopt a cleaner modular architecture using dedicated DAO + service layers,
# as recommended in the supervisor feedback. The updated routing separates 
# TaskDef management, TaskStageDef management, and AgentPipeline execution 
# into self-contained services.
# Conversation Topic: "Rainn Iteration 2 – Modular Flask routing + pipeline runner"
# Date: November 2025
#
# References:
# - Flask Routing – https://flask.palletsprojects.com/
# - SQLite3 Module – https://docs.python.org/3/library/sqlite3.html
# - UCC FYP Bible – Modular design, routing documentation, ChatGPT tagging
# ==========================================

from flask import Flask, render_template, request, redirect, url_for

# Updated service imports (Option B: clean + readable)
from service.task_def_service import TaskDefService
from service.task_stage_def_service import TaskStageService
from service.agent_pipeline_service import AgentPipelineService
from service.agent_process import AgentProcessing

# Initialize Flask app
app = Flask(__name__)

# Service-layer instances
taskdef_service = TaskDefService()
stage_service = TaskStageService()
pipeline_service = AgentPipelineService()
agent_runner = AgentProcessing()


# ==========================================
# HOME / INDEX
# ==========================================
@app.route("/")
def home_page():
    """
    Displays all TaskDefs (agents) and their stages.
    Supervisor advised grouping stages by TaskDef_ID for clarity.
    """

    taskdefs = taskdef_service.list_taskdefs()
    stages = stage_service.list_all_stages()

    # Group stages by TaskDef_ID_FK
    stages_by_agent = {}
    for s in stages:
        stages_by_agent.setdefault(s.TaskDef_ID_FK, []).append(s)

    return render_template(
        "index.html",
        taskdefs=taskdefs,
        stages_by_agent=stages_by_agent
    )


# ==========================================
# DATABASE VIEW (for debugging)
# ==========================================
@app.route("/DbView")
def database_page():
    """
    Displays TaskDefs, TaskStages, and AgentPipelines for debugging.
    """
    return render_template(
        "database_view.html",
        taskdefs=taskdef_service.list_taskdefs(),
        taskstages=stage_service.list_all_stages(),
        pipelines=pipeline_service.list_pipelines()
    )


# ==========================================
# CREATE A TASKDEF (Agent Type)
# ==========================================
@app.route("/add_agent", methods=["GET", "POST"])
def add_agent():
    """
    Adds a new TaskDef and associated TaskStageDef entries.
    Logic split from DAO and moved into TaskDefService / TaskStageService.
    """

    if request.method == "POST":
        name = request.form.get("agent_name")
        desc = request.form.get("agent_description")

        # Create TaskDef
        new_id = taskdef_service.create_taskdef(name, desc)

        # Retrieve user-entered stages
        stage_names = request.form.getlist("stage_name[]")
        stage_descs = request.form.getlist("stage_desc[]")

        for s_name, s_desc in zip(stage_names, stage_descs):
            stage_service.create_stage(new_id, s_name, s_desc)

        return redirect(url_for("home_page"))

    return render_template("add_agent.html")


# ==========================================
# UPDATE TASKDEF (Agent)
# ==========================================
@app.route("/update_agent/<int:taskdef_id>", methods=["GET", "POST"])
def update_agent(taskdef_id):
    """ Updates a TaskDef entry. """

    agent = taskdef_service.get_taskdef_by_id(taskdef_id)
    agent_stages = stage_service.get_stages_for_task(taskdef_id)

    if request.method == "POST":
        name = request.form.get("agent_name")
        desc = request.form.get("agent_description")
        taskdef_service.update_taskdef(taskdef_id, name, desc)
        return redirect(url_for("home_page"))

    return render_template("update_agent.html", agent=agent, stages=agent_stages)


# ==========================================
# UPDATE A STAGE
# ==========================================
@app.route("/update_stage/<int:stage_id>", methods=["GET", "POST"])
def update_stage(stage_id):
    """ Updates a single TaskStageDef entry. """

    stage = stage_service.taskstage_dao.get_TaskStageDef_by_id(stage_id)

    if request.method == "POST":
        updated = stage_service.taskstage_dao.update_TaskStageDef(
            stage.__class__(
                stage.TaskStageDef_ID,
                stage.TaskDef_ID_FK,
                request.form.get("stage_type"),
                request.form.get("stage_desc")
            )
        )
        return redirect(url_for("update_agent", taskdef_id=stage.TaskDef_ID_FK))

    return render_template("update_stage.html", stage=stage)


# ==========================================
# DELETE AN AGENT + STAGES
# ==========================================
@app.route("/delete_agent/<int:taskdef_id>", methods=["POST"])
def delete_agent(taskdef_id):
    """ Deletes a TaskDef and all associated TaskStages. """
    stage_service.delete_stages_for_task(taskdef_id)
    taskdef_service.delete_taskdef(taskdef_id)
    return redirect(url_for("home_page"))


# ==========================================
# ITERATION 2 — AGENT BUILDER (UI)
# ==========================================
@app.route("/agent_builder", methods=["GET", "POST"])
def agent_builder_page():
    """
    Step 1 — User selects a TaskDef (operation) and names their agent.
    Step 2 — This creates an AgentPipeline entry mapped to that TaskDef.
    """

    # Load operations (TaskDefs)
    taskdefs = taskdef_service.list_taskdefs()

    # Detect selected TaskDef
    selected_taskdef = (
        request.args.get("operation_selected") or
        request.form.get("operation_selected")
    )

    # Load stages for preview
    stages = None
    if selected_taskdef:
        selected_taskdef = int(selected_taskdef)
        stages = stage_service.get_stages_for_task(selected_taskdef)

    agent_saved = False
    saved_pipeline_id = None

    if request.method == "POST":

        agent_name = request.form.get("agent_name")
        directory = request.form.get("directory_path")
        task_id = selected_taskdef

        new_pipeline = pipeline_service.create_pipeline(
            user_id=1,
            agent_name=agent_name,
            taskdef_id=task_id,
            directory_path=directory
        )

        agent_saved = True
        saved_pipeline_id = new_pipeline.Input_ID

    return render_template(
        "agent_builder.html",
        taskdefs=taskdefs,
        stages=stages,
        selected_taskdef=selected_taskdef,
        agent_saved=agent_saved,
        saved_pipeline_id=saved_pipeline_id
    )


# ==========================================
# ITERATION 2 — AGENT RUNNER (FILE PATH)
# ==========================================
@app.route("/agent_runner/<int:pipeline_id>", methods=["GET", "POST"])
def agent_runner_page(pipeline_id):
    """
    Runs the agent pipeline using a modular task execution system.
    Supervisor requirement: user-provided file path must be configurable.
    """

    pipeline = pipeline_service.get_pipeline(pipeline_id)
    if not pipeline:
        return "Pipeline not found.", 404

    # Load TaskDef (operation type)
    taskdef = taskdef_service.get_taskdef_by_id(pipeline.Operation_Selected)

    if request.method == "POST":

        file_path = request.form.get("file_path")

        output = agent_runner.run(
            taskdef_id=pipeline.Operation_Selected,
            file_path=file_path
        )

        return render_template(
            "agent_result.html",
            pipeline=pipeline,
            taskdef=taskdef,
            output=output
        )

    return render_template(
        "agent_run.html",
        pipeline=pipeline,
        taskdef=taskdef
    )


if __name__ == "__main__":
    app.run(debug=True)
