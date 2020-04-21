from Patient import *
import uuid

class Hospital:
    def __init__(self, name, capacity):
        self.ID= str(uuid.uuid1())
        self.name = name
        self.capacity = int (capacity) 
        self.patients = [] # List of patients admitted to the hospital 
        self.staff = [] # List of doctors and nurses working in the hospital
        
    
    # return the percentage of occupancy of this hospital 
    def occupancy (self):         
        return 100* len(self.patients) / self.capacity
    
    def absolut (self):
        return self.capacity - len(self.patients) 
    
    # admit a patient to the hospital of given name and date of birth 
    def admission (self, name, dob):         
        p = Patient (name, dob)
        self.patients.append(p)
    
    def discharge (self, name, dob):         
        p = Patient (name, dob)
        self.patients.remove(p)
        
    def serialize(self):
        #print(self.patients)
        return {
            'id': self.ID, 
            'name': self.name, 
            'capacity': self.capacity,
            'occupancy': self.occupancy(),
            'beds left' : self.absolut(),
            'patients': str([x.serialize() for x in self.patients]), #mitjsonify veruschen
        }
    

    