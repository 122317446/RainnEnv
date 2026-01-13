from dao.task_stage_instance_dao import TaskStageInstanceDAO
from model.task_stage_instance import TaskStageInstance


class TaskStageInstanceService:
    """ Service layer for managing TaskStageInstance runtime execution. """

    def __init__(self):
        self.dao = TaskStageInstanceDAO()

    def create_stage_instance(
        self,
        task_instance_id_fk,
        stage_order,
        stage_name,
        status,
        output_artifact_path=None
    ):
        """ Creates a new TaskStageInstance entry. """
        new_stage = TaskStageInstance(
            TaskStageInstance_ID=None,
            TaskInstance_ID_FK=task_instance_id_fk,
            Stage_Order=stage_order,
            Stage_Name=stage_name,
            Status=status,
            Output_Artifact_Path=output_artifact_path,
            Started_At=None,
            Ended_At=None,
            Error_Message=None
        )
        return self.dao.create_stage_instance(new_stage)

    def update_stage_instance(self, stage_instance):
        """ Updates an existing TaskStageInstance entry. """
        return self.dao.update_stage_instance(stage_instance)

    def get_stages_for_task_instance(self, task_instance_id_fk):
        """ Retrieves all stage instances for a given TaskInstance. """
        return self.dao.get_stages_for_task_instance(task_instance_id_fk)
    
    def list_stage_instances(self):
        """ Returns all TaskStageInstance entries (newest first). """
        return self.dao.get_all_stage_instances()

    def mark_stage_completed(self, stage_instance_id, output_artifact_path):
        return self.dao.mark_completed(stage_instance_id, output_artifact_path)

    def mark_stage_failed(self, stage_instance_id, error_message):
        return self.dao.mark_failed(stage_instance_id, error_message)
