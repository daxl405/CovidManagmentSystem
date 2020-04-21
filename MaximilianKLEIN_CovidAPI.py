from flask import Flask, request, jsonify
from CovidManagementSystem import *
from Hospital import * 
from Quarantine import *
from Staff import *
from Patient import *
import numpy as np

app = Flask(__name__)

# Root object for the management system
ms = CovidManagementSystem ()

################################## HOSPITALS ######################################

#Add a new hospital (parameters: name, capacity). 
@app.route("/hospital", methods=["POST"])
def addHospital():
    ms.addHospital(request.args.get('name'), request.args.get('capacity'))   
    return jsonify(f"Added a new hospital called {request.args.get('name')} with capacity {request.args.get('capacity')}")

#Return the details of a hospital of the given hospital_id. 
@app.route("/hospital/<hospital_id>", methods=["GET"])
def hospitalInfo(hospital_id):       
    h = ms.getHospitalById(hospital_id)
    if(h!=None): 
        return jsonify(h.serialize())
    return jsonify(
            success = False, 
            message = "Hospital not found")

# Admission of a patient to a given hospital 
@app.route("/hospital/<hospital_id>/patient", methods=["POST"])
def admitpatient(hospital_id):       
    h = ms.getHospitalById(hospital_id)
    if(h!=None and h.occupancy < 100): 
        h.admission (request.args.get('name'), request.args.get('dob'))  
        return jsonify(
            success = True,
            message = f" Patient {request.args.get('name')} born {request.args.get('dob')} has been admited to the hospital")
    if(h.occupancy > 100):
        return jsonify(
                success = True, 
                message = "This Hospital is unfortunatly full, please choose another one"
                )
    return jsonify(
        success = False, 
        message = "Hospital not found")  
    
@app.route("/hospital/<hospital_id>", methods=["DELETE"])
def deleteHospital(hospital_id):
    
    result = ms.deleteHospital(hospital_id)   
    if(result): 
        message = f"Hospital with id {hospital_id} was deleted" 
    else: 
        message = "Hospital not found" 
    return jsonify(
        success = result, 
        message = message)

@app.route("/hospitals", methods=["GET"])
def allHospitals():   
    return jsonify(hospitals=[h.serialize() for h in ms.getHospitals()])

################################### QUAR. AREA ########################################################################################

@app.route("/quarantine", methods=["POST"])
def addQuarArea():
    ms.addQuarArea(request.args.get('name'), request.args.get('capacity'))
    return jsonify(f"Added a new Quratine Area called {request.args.get('name')} with capacity {request.args.get('capacity')}")

@app.route("/quarantine/<qu_id>", methods=["GET"])
def QuarAreaInfo (qu_id):       
    h = ms.getQuarAreaById(qu_id)
    if(h!=None): 
        return jsonify(h.serialize())
    return jsonify(
            success = False, 
            message = "Area not found")

@app.route("/quarantine/<qu_id>/<pat_id>", methods=["POST"])
def addPatArea(qu_id, pat_id):
    p = ms.getPatientById(pat_id)
    a = ms.getQuarAreaById(qu_id)
    
    if(p != None and a != None): 
        if (p.area == None):
            p.setArea(a)
            a.addPat(p)
            return jsonify(
                success = True, 
                message = "Patient " + pat_id + " has been added to the Area " + qu_id)
        
    else:
        return jsonify(
            success = False, 
            message = "Area or Patient not found")   
    
@app.route("/quarantine/<qu_id>", methods=["DELETE"])
def deleteArea(qu_id):
    
    result = ms.deleteArea(qu_id)   
    if(result): 
        message = f"Area with id {qu_id} was deleted" 
    else: 
        message = "Area not found" 
    return jsonify(
            success = result, 
            message = message)

@app.route("/quarantines", methods=["GET"])
def allAreas(): 
    return jsonify(area=[a.serialize() for a in ms.getAreas()])

################################## STAFF ##########################################
    
@app.route("/staff", methods=["POST"])
def addStaff ():
   ms.addStaff(request.args.get('name'), request.args.get('dob'), request.args.get('role'))
   return jsonify(f"Added a new {request.args.get('role')} named {request.args.get('name')} born the {request.args.get('dob')}")

@app.route("/staff/<staff_id>", methods=["PUT"])
def setWorkingplace(staff_id):
    s = ms.getStaff(staff_id)
    if (s == None):
        return jsonify(
                success = False, 
                message = "No Staff found with that ID!"
                )
    if (s.workingplace != None):
        return jsonify(
                success = False, 
                message = "Staff already work in " + str(s.workingplace))
    else:
        s.workingplace = request.args.get("workplace")
        return jsonify(
                success = True, 
                message = "Staff has been succefully added to a new Facility!")    

@app.route("/staff/<staff_id>", methods=["DELETE"])
def deleteStaff(staff_id):

    result = ms.deleteStaff(staff_id)   
    if(result): 
        message = f"Staff with id {staff_id} was deleted" 
    else: 
        message = "Staff not found" 
    return jsonify(
        success = result, 
        message = message)
        

@app.route("/staff", methods=["GET"])
def allStaff():
    return jsonify(staff=[s.serialize() for s in ms.getStaffs()])
    
################################### PATIENT ################################################
    
@app.route("/patient", methods=["POST"])
def addPatient():
   ms.addPatient(request.args.get('name'), request.args.get('dob'))
   return jsonify(f"Added a new Patient named {request.args.get('name')} and born the {request.args.get('dob')}")   

@app.route("/patient/<pat_id>/admit/<facility_id>", methods=["PUT"])
def admitPatient(pat_id, facility_id):
    p = ms.getPatient(pat_id)
    h = ms.getHospitalById(facility_id)
    a = ms.getQuarAreaById(facility_id)
    
    if (p == None):
        return jsonify(
                success = False, 
                message = "No pat"
                )
    if (a == None and h == None):
        return jsonify(
                success = False, 
                message = "No facility"
                )
    if (a != None and h != None):
        return jsonify(
                success = False, 
                message = "Looks like patient is in more than 1 fac"
                )
    if (a != None):
        p.area = a.ID
        a.admission(p.name, p.dob)
        return jsonify(
            success = True,
            message = "Patient " + p.name + " was succesfully added to qurantine area: " + a.ID#
            )
        
    if (h != None):
        p.area = h.ID
        h.admission(p.name, p.dob)
        return jsonify(
            success = True,
            message = "Patient " + p.name + " was succesfully added to hospital: " + h.ID#
            )
    
@app.route("/patient/<pat_id>/discharge/<facility_id>", methods=["PUT"])
def dischargePatient(pat_id, facility_id):
    p = ms.getPatient(pat_id)
    h = ms.getHospitalById(facility_id)
    a = ms.getQuarAreaById(facility_id)
    
    if (p == None):
        return jsonify(
                success = False, 
                message = "No pat"
                )
    if (a == None and h == None):
        return jsonify(
                success = False, 
                message = "No facility"
                )
    if (a != None and h != None):
        return jsonify(
                success = False, 
                message = "Looks like patient is in more than 1 fac"
                )
    if (a != None):
        p.area = None
        a.discharge
        return jsonify(
            success = True,
            message = "Patient " + p.name + " was succesfully discharged from qurantine area: " + a.ID#
            )      
    if (h != None):
        h.discharge
        p.area = None
        return jsonify(
            success = True,
            message = "Patient " + p.name + " was succesfully discharged from hospital: " + h.ID#
            )
    
@app.route("/patient/<pat_id>/diagnosis", methods=["POST"])
def diagnosis(pat_id):
    p = ms.getPatient(pat_id)
    rn = np.random.randint(1, 101)
    print (rn)
    if (rn < 90):
        p.status = "Discharged"
        return jsonify (
                success = True, 
                message = "Patient " + p.name + "got diagnosed NEGATIVE! Thanks for making the test, you have been discharged!"
                )
        if (p.area != None):
            dischargePatient(pat_id, p.area)
        
    else:
        for a in ms.quarantines:
            if (a.capacity != 0):
                p.area = a.ID
                p.status = "In Isolation"
                addPatArea(a.ID, pat_id)
                
                return jsonify(
                        success = True, 
                        message = "Patient " + p.name + " got diagnosed POSITIVE with COVID-19. He´s been moved to the quarantine area: " + a.name
                        )
            else:
                continue
            
        return jsonify (
                success = False, 
                message = "No place left in any quarantine Areas!"
                )
        
    
@app.route("/patient/<pat_id>/cure", methods=["POST"])
def cure(pat_id):
    p = ms.getPatient(pat_id)
    if (p == None ):
        return jsonify(
                success = False, 
                message = "No patient found with this ID"
                )
        
    rn = np.random.randint(1, 101)
    if (rn >= 97):
        p.status = "Dead"
        dischargePatient(pat_id, p.area)
        
        return jsonify (
                success = True, 
                message = "Patient " + p.name + " couldn´t get cured and died in qurantine!"
                )       
    else: 
        p.status = "Discharged"
        p.area = None
        dischargePatient(pat_id, p.area)
        
        return jsonify(
                success = True, 
                message = "Patient " + p.name + " got cured and is ready to get discharged"
                )         
    
@app.route("/patient", methods=["GET"])
def allPatients():
    return jsonify(patient=[p.serialize() for p in ms.getPatients()])

################################ STATS ################################################

@app.route("/stats", methods=["GET"])
def Stats():
    occupancy_dict = {}      
    for h in ms.hospitals:
        occupancy_dict[h.name] = h.occupancy()
     
    for a in ms.quarantines:
        occupancy_dict[a.name] = a.occupancy()
        
    return jsonify(
            success = True, 
            message = occupancy_dict
            )
    
    patient_status = []
    for p in ms.patients:
        patient_status.append((p.name, p.status))
        return jsonify(
                success = True, 
                message = patient_status
                )

#################################################################################
@app.route("/")
def index():
    return jsonify(
            success = True, 
            message = "Your server is running! Welcome to the Covid API.")

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE"
    return response

if __name__ == "__main__":
    print("Server strarted")
    app.run(debug=False, port=8888)