from Database.AddToDB import *
import subprocess
import os


def ReccomendationToEmployeeByRoom(date_time, occupancy):
    reccomendedList=[]
    for i in xrange(10):
        room = Rooms.find()[i]
        if occupancy<=room.schedule[date_time].occupancy :
            reccomendedList.append(room)
    return reccomendedList

