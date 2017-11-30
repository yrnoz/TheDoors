def main():
    best_rooms = {1: 4, 2: 56, 3: 5, 2: 4}
    sorted_rooms = sorted(best_rooms.items(), key=lambda x: x[1])
    print(sorted_rooms[::-1])
    for x in sorted_rooms:
        print(x[1])


if __name__ == "__main__": main()