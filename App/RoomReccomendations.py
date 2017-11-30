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


# input: time requested to check num of empty places in each room.
# output: a dictionary that for each room include the number of empty seats in that room in the given time.
def emptyRooms(time):
    emptyPlaceInRooms = {}
    for i in xrange(db.collection.count()):
        room = Rooms.find()[i]
        emptyPlaceInRooms.update(room.id, room.maxCapacity-room.schedule[time].occupancy)
    return emptyPlaceInRooms



