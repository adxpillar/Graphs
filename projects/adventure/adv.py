from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
# traversal_path = []


# You start in room `0`, which contains exits `['n', 's', 'w', 'e']`. 
# Start by writing an algorithm that picks a random unexplored direction from the player's current room, 
# travels and logs that direction
# then loops. 

# set up queue 
class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)

# Create Graph 
class Graph():
    def __init__(self, player):
        self.rooms = {}
        self.player = player
        # move traversal into graph class 
        self.traversal_path = []

    # room as vertex 
    # with id 
    # and exit 
    def add_room(self, room_id, room_exits):
        if room_id not in self.rooms:
            self.rooms[room_id] = [{}, ()]
            for exit in room_exits:
                self.rooms[room_id][0][exit] = '?'
        if room_id == 0:
            self.rooms[room_id][1] = (0, 0)

    # add edge between two rooms 
    # with direction to follow
    def add_room_connection(self, room1_id, room2_id, direction):
        movement = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
        if room1_id in self.rooms and room2_id in self.rooms:
            self.rooms[room1_id][0][direction] = room2_id
            self.rooms[room2_id][0][movement[direction]] = room1_id
        else:
            raise IndexError('That room does not exist!,')

    def get_exits(self, room_id):
        return self.rooms[room_id][0]

    def get_coordinates(self, room_id):
        return self.rooms[room_id][1]

    def use_exit(self, direction):
        previous_room = self.player.current_room
        self.player.travel(direction)
        self.traversal_path.append(direction)

        this_room = self.player.current_room
        self.add_room(this_room.id, this_room.get_exits())
        # connnect 
        self.add_room_connection(previous_room.id, this_room.id, direction)

        prev_coordinates = self.get_coordinates(previous_room.id)
        # put direction with flow to go back to previous coordinate
        if direction == 'n':
            new_coordinates = (prev_coordinates[0], prev_coordinates[1] + 1)
        if direction == 's':
            new_coordinates = (prev_coordinates[0], prev_coordinates[1] - 1)
        if direction == 'w':
            new_coordinates = (prev_coordinates[0] - 1, prev_coordinates[1])
        if direction == 'e':
            new_coordinates = (prev_coordinates[0] + 1, prev_coordinates[1])

        self.rooms[this_room.id][1] = new_coordinates
        # check coords
        self.check_coordinates()

        return this_room

    # depth first traversal with recursion 
    def dft_recursive(self, starting_room=None, completed_trip=None):
        starting_room = starting_room or self.player.current_room
        completed_trip = completed_trip or set()
        # kind of baseline 
        if starting_room not in completed_trip:
            self.add_room(starting_room.id, starting_room.get_exits())

            # Pick a random unexplored direction from the player's current room, 
            current_room_id = starting_room.id
            current_room_exits = self.get_exits(current_room_id)

            directions = ['n','e', 'w','s']

            random.shuffle(directions)
            
            # When you reach a dead-end, do recursion to
            # walk back to the nearest room that does contain an unexplored path.

            if directions[0] in current_room_exits and current_room_exits[directions[0]] == '?':
                new_room = self.use_exit(directions[0])
                self.dft_recursive(new_room, completed_trip)
            elif directions[1] in current_room_exits and current_room_exits[directions[1]] == '?':
                new_room = self.use_exit(directions[1])
                self.dft_recursive(new_room, completed_trip)
            elif directions[2] in current_room_exits and current_room_exits[directions[2]] == '?':
                new_room = self.use_exit(directions[2])
                self.dft_recursive(new_room, completed_trip)
            elif directions[3] in current_room_exits and current_room_exits[directions[3]] == '?':
                new_room = self.use_exit(directions[3])
                self.dft_recursive(new_room, completed_trip)
            else:
                # log  
                completed_trip.add(starting_room)


    # You can find the path to the shortest unexplored room by using a breadth-first search
    # BFS will return the path as a list of room IDs. 
    def bfs(self, starting_room=None):
        starting_room = starting_room or self.player.current_room
        queue = Queue()
        queue.enqueue([starting_room.id])
        visited = set()

        while queue.size() > 0:
            self.add_room(starting_room.id, starting_room.get_exits())

            current_path = queue.dequeue()
            current_room_id = current_path[-1]
            current_exits = self.get_exits(current_room_id)

            # we are searching for '?'
            if '?' in current_exits.values():
                self.convert_path(current_path)
                return

            if current_room_id not in visited:
                visited.add(current_room_id)
                for exit in current_exits:
                    path_to_next_room = [*current_path, current_exits[exit]]
                    queue.enqueue(path_to_next_room)


    # BFS will return the path as a list of room IDs. 
    # You will need to convert this to a list of n/s/e/w directions 
    def convert_path(self, list_of_rooms):
        steps_in_path = len(list_of_rooms) - 1
        # loop and get exits from each item in list of path 
        for i in range(steps_in_path):
            current_exits = self.get_exits(list_of_rooms[i]).items()
            next_room = list_of_rooms[i + 1]
            direction = next(
                (direction for direction, room in current_exits if room == next_room), None)
            self.player.travel(direction)
            self.traversal_path.append(direction)
            self.check_coordinates()

    # check coordinates for current room and adjacent rooms 
    # to specify next movement and direct link
    def check_coordinates(self, starting_room=None):
        starting_room = starting_room or self.player.current_room
        # get coord for current room 
        current_coordinates = self.get_coordinates(starting_room.id)
        current_exits = self.get_exits(starting_room.id)
        current_room_id = starting_room.id

        directions = ['n', 's', 'e', 'w']
        # check coords inn each room 
        if directions[0] in current_exits and current_exits[directions[0]] == '?':
            coordinates_to_check = (
                current_coordinates[0], current_coordinates[1] + 1)
            self.check_for_adjacent_room(
                current_room_id, coordinates_to_check, directions[0])

        if directions[1] in current_exits and current_exits[directions[1]] == '?':
            coordinates_to_check = (
                current_coordinates[0], current_coordinates[1] - 1)
            self.check_for_adjacent_room(
                current_room_id, coordinates_to_check, directions[1])

        if directions[2] in current_exits and current_exits[directions[2]] == '?':
            coordinates_to_check = (
                current_coordinates[0] + 1, current_coordinates[1])
            self.check_for_adjacent_room(
                current_room_id, coordinates_to_check, directions[2])

        if directions[3] in current_exits and current_exits[directions[3]] == '?':
            coordinates_to_check = (
                current_coordinates[0] - 1, current_coordinates[1])
            self.check_for_adjacent_room(
                current_room_id, coordinates_to_check, directions[3])

        if directions[0] in current_exits and current_exits[directions[0]] == '?':
            coordinates_to_check = (
                current_coordinates[0], current_coordinates[1] + 1)
            self.check_for_adjacent_room(
                current_room_id, coordinates_to_check, directions[0])

    # use graph logic 
    # check for adjacent rooms and make connection 
    def check_for_adjacent_room(self, current_room_id, adjacent_coordinates, direction):
        room_id = next(
            (id for id, value in self.rooms.items() if value[1] == adjacent_coordinates), None)
        # connect 
        if room_id:
            self.add_room_connection(current_room_id, room_id, direction)


paths_created = []

for i in range(501):
    player = Player(world.starting_room)
    traverse_graph = Graph(player)

    while len(traverse_graph.rooms) < len(room_graph):
        traverse_graph.bfs()
        traverse_graph.dft_recursive()

    paths_created.append(traverse_graph.traversal_path)

shortest_length = len(paths_created[0])
shortest_path = paths_created[0]
for path in paths_created:
    if len(path) < shortest_length:
        shortest_path = path
        shortest_length = len(shortest_path)
traversal_path = shortest_path



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
