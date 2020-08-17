class Bot:

    def __init__(self,data):
        self.data = data

    def should_act(self):
        return self.data.message.startswith('/')
    
    def reply(self):
        if self.should_act:
            return {}'this is Bot Lord'