from Database.AddToDB import *
import subprocess
import os

if __name__ == "__main__":
    p = subprocess.Popen('mongod',stdout=open(os.devnull,"w"))
    Rooms.drop()
    Employees.drop()
    read_employees_details("employees_test.csv")
    read_rooms_details("rooms_test.csv")
    room = Rooms.find()[0]
    print("Finished Testing")
    assign_employees_to_room_one_hour('24/07/17 12', room, 10)
    assign_employees_to_room_to_X_hours('24/07/17 12', 200, 10)
    p.terminate()


