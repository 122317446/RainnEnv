class AgentPipeline:
    def __init__(
        self,
        Input_ID,
        User_ID,
        Agent_Name,
        Text_Input,
        File_Text,
        Operation_Selected,
        Directory_Path,
        Created_At=None
    ):
        self.Input_ID = Input_ID
        self.User_ID = User_ID
        self.Agent_Name = Agent_Name
        self.Text_Input = Text_Input
        self.File_Text = File_Text
        self.Operation_Selected = Operation_Selected
        self.Directory_Path = Directory_Path
        self.Created_At = Created_At



""" NEED TO ADD SELF STR """