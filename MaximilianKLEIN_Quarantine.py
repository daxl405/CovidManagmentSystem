import uuid
class Quarantine:
    def __init__(self, name, capacity):
        self.ID = str(uuid.uuid1())
        self.name = name
        self.capacity = int(capacity)
        self.patients = []
        self.staff = []
        
    def addPat(self, pat_id):
        self.patients.append(pat_id)

    def occupancy (self):         
        return 100* len(self.patients) / self.capacity 

    def absolut (self):
        return self.capacity - len(self.patients) 
    
    def admission (self, name, dob):         
        p = Patient (name, dob)
        self.patients.append(p)
        
    def discharge (self, name, dob):         
        p = Patient (name, dob)
        self.patients.remove(p)
    
    def serialize(self):
        return {
            'id': self.ID, 
            'name': self.name, 
            'capacity': self.capacity,
            'occupancy': self.occupancy(),
            'places left': self.absolut(),
            'patients': str([x.serialize() for x in self.patients]),
        }
    
    
       
        