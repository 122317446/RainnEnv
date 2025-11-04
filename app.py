from flask import*
from service.agent_service import*

app = Flask(__name__)
Agent_Service = AgentService()


@app.route("/")
def get_all_agents_and_stages():
    agents = Agent_Service.list_agents()
    agent_stages = Agent_Service.list_stages()

    stages_by_agent = {}
    for x in agent_stages:
        stages_by_agent.setdefault(x.TaskDef_ID_FK, []).append(x)

    return render_template('index.html', agents=agents, stages_by_agent=stages_by_agent, agent_stages=agent_stages)

@app.route("/DbView")
def database_page():
    agents = Agent_Service.list_agents()
    agent_stages = Agent_Service.list_stages()
    
    return render_template('database_view.html', agents=agents, agent_stages=agent_stages)

  
@app.route('/add_agent', methods=['GET', 'POST'])
def add_agent():
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


@app.route('/get_data_by_id/<int:ID>')
def retreive_specific_data(ID):
    retreived = userinputservice.get_data_details(ID)
    return render_template('indexid.html', retreived=retreived)

@app.route('/update_data/<int:ID>', methods=['POST'])
def update_data(ID):
    retreived = userinputservice.get_data_details(ID)

    retreived.text = request.form.get('changetext')

    userinputservice.update_data(retreived)

    print("The database has been updated!")

    return redirect(url_for("test1"))

@app.route('/delete_agent/<int:agent_id>', methods=['POST'])
def delete_agent(agent_id):
    Agent_Service.delete_agent(agent_id)
    return redirect(url_for('get_all_agents_and_stages'))
