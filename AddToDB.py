import pymongo                      #import the module for the mongoDB
from pymongo import MongoClient

client = MongoClient()          #making the connection with the DB
db = client['test-database']    #create a new DB 
Rooms = db["Rooms"]             #create new table that called Rooms
Employees = db["Employees"]     #create new table that called Employees

#The function gets a CSV file with details about employees in the 
#factory and adds them to the DB
#input: CSV file
#output: side effect  - the details added to the DB
def read_employees_details(inputfile): 
	global Employees
	with open(inputfile) as details:       #open the file
		for line in details.readlines():
			id, name, role, premission = line.split(",")     #get the parameters we need from the line
			premission.rstrip()
			employee = {"id" : str(id), "name" : name, "role" : role, "premission" : str(premission), "friends" : []}
			Employees.insert(employee)     #add employee's details to the DB


#The function gets a CSV file with details about rooms in the 
#factory and adds them to the DB
#input: CSV file
#output: side effect  - the details added to the DB
def read_rooms_details(inputfile):
	global Rooms
	with open(inputfile) as details:      #open the file
		for line in details.readlines():
			id, capacity, premission, floor = line.split(",")        #get the parameters we need from the line
			floor.rstrip()
			room = {"id" : id, "capacity" : str(capacity), "premission" : str(premission), "floor" : str(floor), "schedule" : []}
			Rooms.insert(room)            #add employee's details to the DB




