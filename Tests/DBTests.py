from Database.AddToDB import *
import subprocess
import os

if __name__ == "__main__":
    p = subprocess.Popen('mongod',stdout=open(os.devnull,"w"))
    read_employees_details("employees_test.csv")
    read_rooms_details("rooms_test.csv")
    print "Finished Testing"
    p.terminate()
