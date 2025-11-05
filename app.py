# ==========================================
# File: app.py
# Created in iteration: 1
# Author: Karl Concha
#
# #ChatGPT (OpenAI, 2025) – Assisted in structuring Flask routes, 
# HTML template rendering, and ensuring consistency between DAO calls 
# and service-layer integration under FYP Bible guidelines.
# Conversation Topic: "Rainn Iteration 1 – Flask routing and CRUD integration"
# Date: November 2025
#
# References:
# - Flask Documentation – "Application Setup and Routing" (https://flask.palletsprojects.com/)
# - SQLite Documentation – "Python SQLite3 Module" (https://docs.python.org/3/library/sqlite3.html)
# - UCC IS4470 FYP Bible – Iteration documentation and code referencing requirements.
# ==========================================

from flask import *
from service.agent_service import *

app = Flask(__name__)
Agent_Service = AgentService()

# ------------------------------------------
# Root route
# ------------------------------------------
@app.route("/")
def get_all_agents_and_stages():
    """ Displays all agents and their related stages. 
    ChatGPT helped define dictionary grouping for stages_by_agent. """
    agents = Agent_Service.list_agents()
    agent_stages = Agent_Service.list_stages()

    stages_by_agent = {}
    for x in agent_stages:
        stages_by_agent.setdefault(x.TaskDef_ID_FK, []).append(x)

    return render_template(
        'index.html',
        agents=agents,
        stages_by_agent=stages_by_agent,
        agent_stages=agent_stages
    )

# ------------------------------------------
# Database view route
# ------------------------------------------
@app.route("/DbView")
def database_page():
    """ Displays database view of all agents and stages. """
    agents = Agent_Service.list_agents()
    agent_stages = Agent_Service.list_stages()
    return render_template('database_view.html', agents=agents, agent_stages=agent_stages)

# ------------------------------------------
# Create agent route
# ------------------------------------------
@app.route('/add_agent', methods=['GET', 'POST'])
def add_agent():
    """ Adds a new agent and its stages via form submission. 
    ChatGPT assisted in form data parsing and stage iteration logic. """
    if request.method == 'POST':
        name = request.form.get('agent_name')
        description = request.form.get('agent_description')

        # Create the base agent first
        new_task = TaskDef(None, name, description)
        Agent_Service.taskdef_dao.add_TaskDef(new_task)

        # Get the inserted agent's ID
        agents = Agent_Service.list_agents()
        task_id = agents[-1].TaskDef_ID

        # Retrieve user-entered stages
        stage_names = request.form.getlist('stage_name[]')
        stage_descs = request.form.getlist('stage_desc[]')

        # Add each stage
        for s_name, s_desc in zip(stage_names, stage_descs):
            new_stage = TaskStageDef(None, task_id, s_name, s_desc)
            Agent_Service.taskstage_dao.add_TaskStageDef(new_stage)

        return redirect(url_for('get_all_agents_and_stages'))

    return render_template('add_agent.html')

# ------------------------------------------
# Update agent route
# ------------------------------------------
@app.route('/update_agent/<int:agent_id>', methods=['GET', 'POST'])
def update_agent(agent_id):
    """ Updates an existing agent details and its stages. """
    agent = Agent_Service.get_agent_by_id(agent_id)
    stage = Agent_Service.get_agent_stages_by_id(agent_id)

    if request.method == 'POST':
        name = request.form.get('agent_name')
        description = request.form.get('agent_description')
        Agent_Service.update_agent_details(agent_id, name, description)
        return redirect(url_for('get_all_agents_and_stages'))

    return render_template('update_agent.html', agent=agent, stages=[stage])

# ------------------------------------------
# Update stage route
# ------------------------------------------
@app.route('/update_stage/<int:stage_id>', methods=['GET', 'POST'])
def update_stage(stage_id):
    """ Updates a single stage within an agent. """
    stage = Agent_Service.taskstage_dao.get_TaskStageDef_by_id(stage_id)

    if request.method == 'POST':
        stage_type = request.form.get('stage_type')
        stage_desc = request.form.get('stage_desc')

        updated_stage = TaskStageDef(
            stage.TaskStageDef_ID,
            stage.TaskDef_ID_FK,
            stage_type,
            stage_desc
        )
        Agent_Service.taskstage_dao.update_TaskStageDef(updated_stage)
        return redirect(url_for('update_agent', agent_id=stage.TaskDef_ID_FK))

    return render_template('update_stage.html', stage=stage)

# ------------------------------------------
# Delete agent route
# ------------------------------------------
@app.route('/delete_agent/<int:agent_id>', methods=['POST'])
def delete_agent(agent_id):
    """ Deletes an agent and all associated stages. """
    Agent_Service.delete_agent(agent_id)
    return redirect(url_for('get_all_agents_and_stages'))


if __name__ == "__main__":
    app.run(debug=True)
