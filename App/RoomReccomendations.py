from Database.AddToDB import *
import subprocess
import os


def reccomendationToEmployeeByRoom(date_time, occupancy):
    reccomendedList=[]
    for i in xrange(db.collection.count()):
        room = Rooms.find()[i]
        if occupancy<=room.maxCapacity-room.schedule[date_time].occupancy:
            reccomendedList.append(room)
    return reccomendedList

