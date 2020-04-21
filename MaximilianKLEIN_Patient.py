import uuid

class Patient:
    def __init__(self, name, dob):
        self.ID = str(uuid.uuid1())
        self.name = name
        self.dob = dob 
        self.area = None
        self.status = None
        
    def setArea(self, area_id):
        self.area = area_id
        
   #in order to make the REMOVE methode work
    def __eq__ (self, other):
        if not isinstance(other, Patient):
            return False
        return self.ID == other.ID         
        
    def serialize(self):
        return {
            'id': self.ID, 
            'name': self.name, 
            'dob': self.dob,
            'area' : self.area,
            'status' : self.status,
        }