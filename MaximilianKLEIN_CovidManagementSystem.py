from Hospital import *
from Quarantine import *
from Patient import *
from Staff import *


class CovidManagementSystem:    
    def __init__(self):
        self.hospitals = [] 
        self.quarantines = []
        self.patients = []
        self.staffs = [] 
        # list of hospitals, areas, patients and staff known to the system
        
############################ HOSPITALS ########################################
        
    def getHospitals (self): 
        return self.hospitals

    def addHospital (self, name, capacity): 
        h = Hospital (name, capacity)
        self.hospitals.append(h)
    
    def getHospitalById(self, id_): 
        for h in self.hospitals: 
            if(h.ID==id_):
                return h
        return None 
    
    def deleteHospital (self, id_):
        h = self.getHospitalById(id_)
        if(h!=None): 
            self.hospitals.remove (h)
        return h!=None                
                
############################### QUARANTINE AREAS ################################
        
    def getAreas (self):
        return self.quarantines
    
    def addQuarArea(self, name, capacity):
        a = Quarantine (name, capacity)
        self.quarantines.append(a)
    
    def getQuarAreaById(self, id_): 
        for a in self.quarantines: 
            if(a.ID==id_):
                return a
        return None 
    
    def getPatientById(self, id_): 
        for p in self.patients: 
            if(p.ID==id_):
                return p  
    
    def deleteArea (self, id_):
        a = self.getQuarAreaById(id_)
        if(a!=None): 
            self.quarantines.remove (a)
        return a!=None     

            
############################## STAFF MEMBERS ###################################
                
    def getStaffs(self):
        return self.staffs
    
    def getStaff(self, id_):
        for s in self.staffs:
            if s.ID == id_:
                return s
        return None
        
        
    def addStaff (self, name, dob, role):
        s = Staff (name, dob, role)
        self.staffs.append(s)
        
    def getStaffById (self, id_):
        for s in self.staffs: 
            if(s.ID==id_):
                return s
        return None
    
    def deleteStaff (self, id_):
        s = self.getStaffById(id_)
        if(s!=None): 
            self.staffs.remove (s)
        return s!=None     
    
############################# PATIENTS #######################################
        
    def getPatients(self):
        return self.patients
    
    def getPatient(self, id_ ):
        for p in self.patients:
            if p.ID == id_:
                return p
        return None        
    
    def addPatient(self, name, dob):
        p = Patient (name, dob)
        self.patients.append(p)
        