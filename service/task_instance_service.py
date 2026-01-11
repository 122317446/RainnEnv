from dao.task_instance_dao import TaskInstanceDAO
from model.task_instance import TaskInstance


class TaskInstanceService:
    """ Service layer for managing TaskInstance runtime execution. """

    def __init__(self):
        self.dao = TaskInstanceDAO()

    def create_task_instance(self, process_id_fk, taskdef_id_fk, status, run_folder):
        """ Creates a new TaskInstance entry. """
        new_instance = TaskInstance(
            TaskInstance_ID=None,
            Process_ID_FK=process_id_fk,
            TaskDef_ID_FK=taskdef_id_fk,
            Status=status,
            Run_Folder=run_folder,
            Created_At=None,
            Updated_At=None
        )
        return self.dao.create_task_instance(new_instance)

    def get_task_instance(self, task_instance_id):
        """ Retrieves a TaskInstance by ID. """
        return self.dao.get_task_instance_by_id(task_instance_id)
    
    def list_task_instances(self):
        """ Returns all TaskInstance entries (newest first). """
        return self.dao.get_all_task_instances()


    def update_task_instance(self, task_instance):
        """ Updates an existing TaskInstance entry. """
        return self.dao.update_task_instance(task_instance)
