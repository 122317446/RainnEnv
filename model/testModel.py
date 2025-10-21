class Userinputs:

    def __init__(self, ID, text):
        
        self.ID = ID
        self.text = text

    def to_dict(self):
        return {
            "ID": self.ID,
            "text": self.text
        }