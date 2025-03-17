class SpedErrors:
    def __init__(self):
        self.errors = []
    
    def add_error(self, message):
        self.errors.append(message)
    
    def get_errors(self):
        return self.errors
