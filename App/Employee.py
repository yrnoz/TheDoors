class Employee:
    def __init__(self, id, name, access_permission):
        self.id = id
        self.name = name
        self.access_permission = access_permission
        self.friends = []
        self.schedule = {}
        self.location = None

    def entrance_room(self, room):
        self.location = room

    def exit_room(self):
        self.location = None

    def recommendation_by_friends(self):
        """"return sorted list of rooms 'sorted_room' sorted by friends location"""
        best_rooms = {}
        for friend in self.friends:
            if friend.location is not None:
                count = best_rooms.get(friend.location, 0) + 1
                best_rooms += {friend.location, count}
        sorted_rooms = sorted(best_rooms.items(),  key=lambda x: x[1])
        return sorted_rooms.reverse()


def main():
    dicttmp = {1 : 4  , 2 : 5,  3 :2  ,4:1 , 5:9 }
    sorted_rooms = sorted(dicttmp.items(),  key=lambda x: x[1])
    sorted_rooms =sorted_rooms[::-1]
    print(sorted_rooms)


if __name__ == "__main__":main()
