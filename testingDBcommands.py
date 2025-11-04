from dao.task_def_dao import TaskDefDAO
from dao.task_stage_def_dao import TaskStageDefDAO
from model.task_def import TaskDef
from model.task_stage_def import TaskStageDef

# Initialise DAOs
taskdef_dao = TaskDefDAO()
taskstage_dao = TaskStageDefDAO()

# 1️⃣ Add task definition
new_task = TaskDef(None, "Diego", "Summarises uploaded resumes")
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

# 5️⃣ Add another task definition (Sylvia - Sentiment Analyser)
new_task_2 = TaskDef(None, "Sylvia", "Analyses sentiment from text or documents")
taskdef_dao.add_TaskDef(new_task_2)

# Fetch all tasks again to get Sylvia’s new ID
tasks = taskdef_dao.get_all_TaskDefs()

# Find the new task (Sylvia)
sylvia_task = next((t for t in tasks if t.TaskDef_Name == "Sylvia"), None)

if sylvia_task:
    # 6️⃣ Add stages for Sylvia
    stage1 = TaskStageDef(
        None, sylvia_task.TaskDef_ID, 
        "Input", 
        "Get the inputs from a document or text"
    )
    stage2 = TaskStageDef(
        None, sylvia_task.TaskDef_ID, 
        "Understand", 
        "Analyse and interpret the text for sentiment"
    )
    stage3 = TaskStageDef(
        None, sylvia_task.TaskDef_ID, 
        "Output", 
        "Output the sentiment results in a Word format or visual chart"
    )

    taskstage_dao.add_TaskStageDef(stage1)
    taskstage_dao.add_TaskStageDef(stage2)
    taskstage_dao.add_TaskStageDef(stage3)

    print("\n✅ Sylvia task and stages successfully added!")
else:
    print("\n❌ Sylvia task not found — please check if the TaskDefDAO added it correctly.")

# 7️⃣ Optional: Display Sylvia’s task and its stages
print("\n--- All Tasks After Adding Sylvia ---")
for t in tasks:
    print(t.to_dict())

print("\n--- All Stages ---")
stages = taskstage_dao.get_all_TaskStageDefs()
for s in stages:
    print(s.to_dict())
