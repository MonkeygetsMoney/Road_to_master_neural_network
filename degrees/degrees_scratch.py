import csv
import sys

from degrees.util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    name1 = input("Name: ")
    name2 = input('Name: ')
    source = shortest_path(name1, name2)
    if source is None:
        sys.exit("Person not found.")
    else:
        print(source)
        #print(movies)
        #print(people)
        # print(movies)
    # target = person_id_for_name(input("Name: "))
    # if target is None:
    #     sys.exit("Person not found.")

    # path = shortest_path(source, target)

    # if path is None:
    #     print("Not connected.")
    # else:
    #     degrees = len(path)
    #     print(f"{degrees} degrees of separation.")
    #     path = [(None, source)] + path
    #     for i in range(degrees):
    #         person1 = people[path[i][1]]["name"]
    #         person2 = people[path[i + 1][1]]["name"]
    #         movie = movies[path[i + 1][0]]["title"]
    #         print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    stack = StackFrontier() # last-in first-out
    queue = QueueFrontier()

    name1 = source.lower()
    name2 = target.lower()
    if name1 in names and name2 in names:
        for name in names:
            if name1 == name:
                # use loop to get the value of name (since it's in a dict)
                for value in names[name]:
                    name1_id = value
                    # use this as the root, initial state

            if name2 == name:
                for value in names[name]:
                    name2_id = value # this is the goal state

    # try to get the movies the actor starred in
    if name1_id in people:
        for person in people:
            if name1_id == person:
                movie_ids = people[person]['movies']

    starred_list = []
    for movie_id in movie_ids:
        # starred_list.append(movie_id)
        for movie in movies:
            if movie == movie_id:
                starred_list.append(movies[movie_id]['stars'])

    # set up node
    initial_state = Node(state=name1_id, parent=None, action=None)
    queue.add(initial_state) 
    goal_state = name2_id
    state_explored = []
    # path explored doesn't mean it's the path that lead to the goal
    while True:
        if queue.empty():
            print('frontier is empty')
            return None
        else:
            node = queue.remove()
            if node.state == goal_state:
                actions = []
                cells = []
                combine = []

                # working backward to find the path to the goal
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()

                for i in range(len(actions)):
                    combine.append((actions[i], cells[i]))

                return combine
            else:
                    # if node.action is not None:
                    #     state_explored.append((node.state, node.action))
                    # else:
                state_explored.append(node.state)

                    # find the neighbor frontier
                for action, state in neighbors_for_person(node.state):
                        # check if the node is already in the frontier or in the explored state
                    if not queue.contains_state(state) and state not in state_explored:
                            # set up new node
                        child = Node(state=state, parent=node, action=action)
                        queue.add(child)


    # TODO
    raise NotImplementedError


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"] # add the pperson into the dictionary
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
