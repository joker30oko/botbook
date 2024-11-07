EDIT_MSG_DELAY = 5
error_message = False
MSG_FATAL_ERRORS = ['5.7.9 Please log in with your web browser and then try again', ]


class BotConfig():
    def __init__(self, delay=2):
        self.delay = delay
        self.admins = [7777020653]
        self.users = []
        self.count_messages = 300
        self.generation = False
        self.error_message = False
        self.count_errors = 0
    
    def update_delay(self, new_delay):
        self.delay = new_delay
        
    def get_delay(self):
        return self.delay
    
    def set_admin(self, id):
        self.admins.append(id)
        
    def set_user(self, id):
        self.users.append(id)

    def get_users(self):
        return self.users

    def get_admins(self):
        return self.admins
    
    def update_count_messages(self, count_messages):
        self.count_messages = count_messages
    
    def get_count_messages(self):
        return self.count_messages
    
    def get_generation(self):
        return self.generation
    
    def update_generation(self):
        if self.generation:
            self.generation = False
        else:
            self.generation = True
            
    def update_error(self, has_error: bool):
        self.error_message = has_error
    
    def get_status_error(self):
        return self.error_message
    
    def get_count_errors(self):
        return self.count_errors


config = BotConfig()
