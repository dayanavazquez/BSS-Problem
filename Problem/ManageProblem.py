class BSS():

    def __init__(self):
        self.INSTANCE_PROBLEM = "i"
        self.PASSENGER_LIST = []
        self.DISPLACE = 3.0
        self.MAX_DISTANCE_WALK = 300.0
        self.MAX_BUS_STOP = 10
        self.MAX_COORDINATE = 20.0
        self.MIN_COORDINATE = 20.0
        self.METAHEURISTIC = "m"

class Point():

    def __init__(self, coordinate_x: float, coordinate_y: float):
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y

    def __str__(self):
        return f'( X: {self.coordinate_x}, Y: {self.coordinate_y} )'

class Passenger():

    def __init__(self, location: Point, id):
        self.location = location
        self.id = id

    def __str__(self,):
        return f"ID: {self.id}  Location: { str(self.location) }"

class BusStop():

    def __init__(self, location: Point, id, passengers_list = []):
        self.location = location
        self.id = id
        self.passenger_list: list = passengers_list if passengers_list else []

    def __str__(self):
        return f"ID: {self.id}  Total Passengers assigned: {len(self.passenger_list)}  Location: { str(self.location) }"

    def inspect_passengers_assigned(self):
        for passenger in self.passenger_list:
            print(str(passenger))

        print("\n")

def generate_bus_stop(coordinate_x, coordinate_y, id):
    return BusStop(
        location=Point(coordinate_x=coordinate_x, coordinate_y=coordinate_y),
        id=id
    )