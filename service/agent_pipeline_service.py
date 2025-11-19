# ==========================================
# File: agent_pipeline_service.py
# Created in iteration: 2
# Author: Karl Concha
#
# #ChatGPT (OpenAI, 2025) – Assisted in creating a dedicated service layer
# for AgentPipeline to separate business logic from DAO and follow the
# FYP Bible modular architecture guidelines.
# ==========================================

from dao.agent_pipeline_dao import AgentPipelineDAO
from model.agent_pipeline import AgentPipeline

class AgentPipelineService:
    """ Service layer for managing stored Agent Pipelines. """

    def __init__(self):
        self.dao = AgentPipelineDAO()

    def create_pipeline(self, user_id, agent_name, taskdef_id):
        new_pipeline = AgentPipeline(
            Pipeline_ID=None,
            User_ID=user_id,
            Agent_Name=agent_name,
            Operation_Selected=taskdef_id,
            Created_At=None
        )
        return self.dao.add_AgentPipeline(new_pipeline)


    def get_pipeline(self, pipeline_id):
        """ Retrieves a pipeline by ID. """
        return self.dao.get_AgentPipeline_by_id(pipeline_id)

    def list_pipelines(self):
        """ Returns all stored pipelines. """
        return self.dao.get_all_AgentPipelines()

    def update_directory(self, pipeline_id, directory_path):
        """ Updates the folder/file path stored in AgentPipeline. """
        pipeline = self.dao.get_AgentPipeline_by_id(pipeline_id)
        if not pipeline:
            return None

        pipeline.Directory_Path = directory_path
        self.dao.update_AgentPipeline(pipeline)
        return pipeline

    def update_pipeline(self, agent_pipeline):
        """ Full update handler. """
        self.dao.update_AgentPipeline(agent_pipeline)

    def delete_pipeline(self, pipeline_id):
        """ Deletes a pipeline record. """
        return self.dao.delete_AgentPipeline(pipeline_id)
