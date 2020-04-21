import uuid
    
class Staff:
    def __init__(self, name, dob, role):
        self.ID = str(uuid.uuid1())
        self.name = name
        self.dob = dob
        self.role = role
        self.workingplace = None

    def serialize(self):
        return {
            'id': self.ID, 
            'name': self.name, 
            'role': self.role,
            'workingplace': self.workingplace,
        }