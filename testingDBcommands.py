from dao.task_def_dao import TaskDefDAO
from dao.task_stage_def_dao import TaskStageDefDAO
from model.task_def import TaskDef
from model.task_stage_def import TaskStageDef

# Initialise DAOs
taskdef_dao = TaskDefDAO()
taskstage_dao = TaskStageDefDAO()

# 1️⃣ Add task definition
new_task = TaskDef(None, "Summarise CVs", "Summarises uploaded resumes")
taskdef_dao.add_TaskDef(new_task)

# 2️⃣ Fetch all tasks and display them
tasks = taskdef_dao.get_all_TaskDefs()
for t in tasks:
    print("\n--- Task Definition ---")
    print(t.to_dict())

# 3️⃣ Add stages (Input, Summarise, Output) for the first task
first_task_id = tasks[0].TaskDef_ID

input_stage = TaskStageDef(None, first_task_id, "Input", "Upload CV files")
summarise_stage = TaskStageDef(None, first_task_id, "Summarise", "Summarise CV content using AI")
output_stage = TaskStageDef(None, first_task_id, "Output", "Display or export the summary results")

taskstage_dao.add_TaskStageDef(input_stage)
taskstage_dao.add_TaskStageDef(summarise_stage)
taskstage_dao.add_TaskStageDef(output_stage)

# 4️⃣ Fetch all stages and display them
stages = taskstage_dao.get_all_TaskStageDefs()
for s in stages:
    print("\n--- Stage Definition ---")
    print(s.to_dict())
