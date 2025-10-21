from DAO.testDAO import testDAO

class UserinputsService:
    def __init__(self):
        self.test_dao = testDAO()
    
    def get_all_data(self):
        return self.test_dao.get_all_Userinputs()
    
    def get_data_details(self, ID): 
        return self.test_dao.get_Userinputs_by_id(ID)
    
    def add_data(self, input): 
        return self.test_dao.add_Userinputs(input)
    
    def update_data(self, input):
        return self.test_dao.update_Userinputs(input)
    
    def delete_data(self, ID):
        return self.test_dao.delete_Userinputs(ID)