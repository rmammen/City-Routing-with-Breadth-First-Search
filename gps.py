import collections
import sys 
import argparse

class City:
    """
    Represents a city with a name and neighboring cities.
    
    Attributes:
        name (str): Name of the city.
        neighbors (dict): Dictionary of neighboring cities with distance and interstate information.
    """
    def __init__(self, name, neighbors):
        """
        Initializes a City object.

        Args:
            name (str): Name of the city.
            neighbors (dict): Dictionary containing neighboring cities as keys
                              and a tuple of distance and interstate as values.
        """
        self.name = name
        self.neighbors = neighbors

    def __repr__(self):
        """
        Returns a string representation of the city.

        Returns:
            str: The name of the city.
        """
        return str(self.name)

    def add_neighbor(self, neighbor, distance, interstate):
        """
        Adds a neighboring city to the current city.

        Args:
            neighbor (City): Neighboring city object.
            distance (float): Distance to the neighboring city.
            interstate (str): Interstate name to reach the neighboring city.
        """
        if neighbor not in self.neighbors:
            self.neighbors[neighbor] = (distance, interstate)
        if self not in neighbor.neighbors:
            neighbor.neighbors[self] = (distance, interstate)

class Map:
    """
    Represents a map containing cities and their relationships.
    
    Attributes:
        cities (list): List of City objects.
        relationships (dict): Dictionary mapping city names to their neighboring cities and distances.
    """
    def __init__(self, relationships):
        """
        Initializes the Map object.

        Args:
            relationships (dict): Dictionary containing city names as keys and a list of tuples
                                  with neighboring city names, distances, and interstates as values.
        """
        self.cities = []
        self.relationships = relationships
        
        # Build the map using the relationships
        for city_name in relationships.keys():
            city = self.get_city(city_name)
            if not city:
                city = City(city_name, {})
                self.cities.append(city)
            
            for neighbor_city_name, neighbor_distance, neighbor_interstate in relationships[city_name]:
                neighbor = self.get_city(neighbor_city_name)
                if not neighbor:
                    neighbor = City(neighbor_city_name, {})
                    self.cities.append(neighbor)
                
                city.add_neighbor(neighbor, neighbor_distance, neighbor_interstate)

    def get_city(self, name):
        """
        Returns a city object by its name.

        Args:
            name (str): Name of the city.

        Returns:
            City: City object if found, None otherwise.
        """
        for city in self.cities:
            if city.name == name:
                return city
        return None

def bfs(graph, start, goal):
    """
    Performs a Breadth-First Search (BFS) to find the shortest path between two cities.

    Args:
        graph (Map): The map containing cities and their connections.
        start (str): Starting city name.
        goal (str): Destination city name.

    Returns:
        list: List of city names representing the shortest path from start to goal.
              Returns None if no path is found.
    """
    explored = []
    queue = collections.deque([[start]])
    
    while queue:
        curr_path = queue.popleft()
        last_node = curr_path[-1]

        if last_node not in explored:
            # Get the current city object
            city = graph.get_city(last_node)
            if city and city.neighbors:
                for neighbor in city.neighbors:
                    # Create a new path by adding the neighbor
                    new_path = curr_path + [neighbor.name]
                    if neighbor.name == goal:
                        return new_path
                    queue.append(new_path)

            explored.append(last_node)

    print("No Path Found")
    return None

def main(start, destination, connections):
    """
    Main function to initialize the map and find the shortest path between two cities.

    Args:
        start (str): Starting city name.
        destination (str): Destination city name.
        connections (dict): Dictionary containing city connections.

    Returns:
        str: Instructions for the route from start to destination.
    """
    try:
        road_map = Map(connections)
        instructions = bfs(road_map, start, destination)
        if not instructions:
            return "No path found"

        output = ""
        for i, city in enumerate(instructions):
            if i == 0:
                msg = f"Starting at {city}"
            elif i < len(instructions) - 1:
                next_city = instructions[i + 1]
                current_city = road_map.get_city(city)
                distance, interstate = current_city.neighbors[road_map.get_city(next_city)]
                msg = f"Drive {distance} miles on {interstate} towards {next_city}, then"
            else:
                msg = "You will arrive at your destination"
            print(msg)
            output += msg + "\n"

        return output
    except Exception as e:
        print(f"Error: {e}")
        
def parse_args(args_list):
    """Takes a list of strings from the command prompt and passes them through as
    arguments.
    
    Args:
        args_list (list): the list of strings from the command prompt
        
    Returns:
        args (ArgumentParser)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--starting_city', type=str, help='The starting city in a route.')
    parser.add_argument('--destination_city', type=str, help='The destination city in a route.')
    args = parser.parse_args(args_list)
    return args

if __name__ == "__main__":
    connections = {
        "Baltimore": [("Washington", 39, "95"), ("Philadelphia", 106, "95")],
        "Washington": [("Baltimore", 39, "95"), ("Fredericksburg", 53, "95"), ("Bedford", 137, "70"), ("Philadelphia", 139, "95")],
        "Fredericksburg": [("Washington", 53, "95"), ("Richmond", 60, "95")],
        "Richmond": [("Charlottesville", 71, "64"), ("Williamsburg", 51, "64"), ("Durham", 151, "85"), ("Fredericksburg", 60, "95"), ("Raleigh", 171, "95")],
        "Durham": [("Richmond", 151, "85"), ("Raleigh", 29, "40"), ("Greensboro", 54, "40")],
        "Raleigh": [("Durham", 29, "40"), ("Wilmington", 129, "40"), ("Richmond", 171, "95")],
        "Greensboro": [("Charlotte", 92, "85"), ("Durham", 54, "40"), ("Ashville", 173, "40")],
        "Ashville": [("Greensboro", 173, "40"), ("Charlotte", 130, "40"), ("Knoxville", 116, "40"), ("Atlanta", 208, "85")],
        "Charlotte": [("Atlanta", 245, "85"), ("Ashville", 130, "40"), ("Greensboro", 92, "85")],
        "Jacksonville": [("Atlanta", 346, "75"), ("Tallahassee", 164, "10"), ("Daytona Beach", 86, "95")],
        "Daytona Beach": [("Orlando", 56, "4"), ("Miami", 95, "268"), ("Jacksonville", 86, "95")],
        "Orlando": [("Tampa", 94, "4"), ("Daytona Beach", 56, "4")],
        "Tampa": [("Miami", 281, "75"), ("Orlando", 94, "4"), ("Atlanta", 456, "75"), ("Tallahassee", 243, "98")],
        "Atlanta": [("Charlotte", 245, "85"), ("Ashville", 208, "85"), ("Chattanooga", 118, "75"), ("Macon", 83, "75"), ("Tampa", 456, "75"), ("Jacksonville", 346, "75"), ("Tallahassee", 273, "27")],
        "Chattanooga": [("Atlanta", 118, "75"), ("Knoxville", 112, "75"), ("Nashville", 134, "24"), ("Birmingham", 148, "59")],
        "Knoxville": [("Chattanooga", 112,"75"), ("Lexington", 172, "75"), ("Nashville", 180, "40"), ("Ashville", 116, "40")],
        "Nashville": [("Knoxville", 180, "40"), ("Chattanooga", 134, "24"), ("Birmingham", 191, "65"), ("Memphis", 212, "40"), ("Louisville", 176, "65")],
        "Louisville": [("Nashville", 176, "65"), ("Cincinnati", 100, "71"), ("Indianapolis", 114, "65"), ("St. Louis", 260, "64"), ("Lexington", 78, "64")],
        "Cincinnati": [("Louisville", 100, "71"), ("Indianapolis", 112, "74"), ("Columbus", 107, "71"), ("Lexington", 83, "75"), ("Detroit", 263, "75")],
        "Columbus": [("Cincinnati", 107, "71"), ("Indianapolis", 176, "70"), ("Cleveland", 143, "71"), ("Pittsburgh", 185, "70")],
        "Detroit": [("Cincinnati", 263, "75"), ("Chicago", 282, "94"), ("Mississauga", 218, "401")],
        "Cleveland": [("Chicago", 344, "90"), ("Columbus", 143, "71"), ("Youngstown", 75, "80"), ("Buffalo", 194, "90")],
        "Youngstown": [("Pittsburgh", 67, "76"), ("Cleveland", 75, "80")],
        "Indianapolis": [("Columbus", 176, "70"), ("Cincinnati", 112, "74"), ("St. Louis", 242, "70"), ("Chicago", 182, "65"), ("Louisville", 114, "65"), ("Mississauga", 498, "401")],
        "Pittsburgh": [("Columbus", 185, "70"), ("Youngstown", 67, "76"), ("Philadelphia", 305, "76"), ("New York", 389, "76"), ("Bedford", 107, "76")],
        "Bedford": [("Pittsburgh", 107, "76"), ("Washington", 137, "70")],
        "Chicago": [("Indianapolis", 182, "65"), ("St. Louis", 297, "55"), ("Milwaukee", 92, "94"), ("Detroit", 282, "94"), ("Cleveland", 344, "90")],
        "New York": [("Philadelphia", 95, "95"), ("Albany", 156, "87"), ("Scranton", 121, "80"), ("Providence", 181, "95"), ("Pittsburgh", 389, "76")],
        "Scranton": [("Syracuse", 130, "81"), ("New York", 121, "80")],
        "Philadelphia": [("Washington", 139, "95"), ("Pittsburgh", 305, "76"), ("Baltimore", 106, "95"), ("New York", 95, "95")]
    }

    args = parse_args(sys.argv[1:])
    main(args.starting_city, args.destination_city, connections) 