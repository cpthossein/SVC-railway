import time
import datetime


class Line:
    def __init__(self, name, origin, destination, num_stations, stations: list, distance_of_stations, *args, **kwargs):
        self.name = name
        self.origin = origin
        self.destination = destination
        self.num_stations = num_stations
        self.stations = stations
        self.distance_of_stations = distance_of_stations

    def __str__(self):
        return f"The line called {self.name} starts from {self.origin} and ends in {self.destination}.\nIt has {self.num_stations} stations which are called respectively " + "".join([f"{self.stations[i]}, " for i in range(self.num_stations-1)]) + f"{self.stations[-1]}.\n" + "".join([f"The distance between {self.stations[i]} and {self.stations[i+1]} is {self.distance_of_stations[i]}.\n" for i in range(self.num_stations-1)])

    def info(self):
        return {'name': self.name, 'origin': self.origin, 'destination': self.destination, 'num_stations': self.num_stations, 'stations': self.stations, 'distance_of_stations': self.distance_of_stations}

    def get_name(self):
        return self.name

    def get_stations(self):
        return self.stations

    def set_name(self, new_name):
        self.name = new_name

    def set_origin(self, new_origin):
        self.origin = new_origin
        self.stations[0] = new_origin

    def set_destination(self, new_destination):
        self.destination = new_destination
        self.destination[-1] = new_destination

    def set_stations(self, new_num_stations, new_stations, new_distance_of_stations):
        self.num_stations = new_num_stations
        self.stations = new_stations
        self.distance_of_stations = new_distance_of_stations


class Train:
    # optional attributes : date , departure_time, ...
    def __init__(self, id, name, line: Line, velocity, stops, stars, ticket_price, route_capacity, departure_time, *args, **kwargs):
        self.id = id
        self.name = name
        self.line = line
        self.velocity = velocity
        self.stops = [0]
        self.stops.extend(stops)
        self.stars = stars
        self.ticket_price = ticket_price
        self.route_capacity = route_capacity
        self.capacity = route_capacity
        self.departure_time = datetime.datetime.strptime(
            departure_time, "%Y-%m-%d %H-%M-%S")
        self.arrival_time = [self.departure_time]
        self.arrival_time_str = []
        for i in range(int(self.line.num_stations)+1):
            self.arrival_time.append(self.arrival_time[-1] + datetime.timedelta(
                hours=self.line.distance_of_stations[i]/velocity, minutes=self.stops[i]))
        self.passengers = []
        self.passengers_str = []
        for element in self.arrival_time:
            self.arrival_time_str.append(element.strftime("%Y-%m-%d %H-%M-%S"))
    
    def __str__(self):
        return f"The train is called {self.name} and its id is {self.id}.\nIt travels at a speed of {self.velocity} km/h on line {self.line.get_name()}.\nThe departure time is {self.departure_time.strftime("%Y-%m-%d %H-%M-%S")}" + "".join([f"It stops at station {element} for {self.stops[element]} minutes.\n" for element in self.line.stations]) + f" This train has {self.stars} stars and a route capacity of {self.route_capacity} passengers. The remaining capacity is {self.capacity} passengers.\nIts ticket price is {self.ticket_price} dollars."

    def info(self):
        return {"name": self.name, "Id": self.id, "line_name": self.line.name, "stop time in each station": self.stops, "stars": self.stars, "average speed": self.velocity, "ticket price": self.ticket_price, "total capacity": self.route_capacity, "remaining capacity": self.capacity, "passegers": self.passengers_str, "departure time": self.departure_time.strftime("%Y-%m-%d %H-%M-%S"), "arrival time": self.arrival_time_str}

    def costumer_info(self):
        return f"The train is called {self.name} and its departure time is {self.departure_time.strftime("%Y-%m-%d %H-%M-%S")}.\nThis train has {self.stars} stars and the ticket price is {self.ticket_price} dollars.\nIt will stop at stations below\n" + "".join(f"{element}\n" for element in self.line.stations) + f"There are {self.capacity} seats available."

    def get_id(self):
        return self.id

    def is_available(self, passengers):
        if self.capacity < passengers:
            return False
        return True

    def add_passenger(self, list_of_passengers):
        self.passengers.extend(list_of_passengers)
        for element in list_of_passengers:
            self.passengers_str.append(element.info())

    def sell_tickets(self, passengers):
        self.capacity -= passengers

    def get_ticket_price(self):
        return self.ticket_price

    def get_line(self):
        return self.line

    def get_stop(self, station):
        idx = self.line.get_stations().index(station)
        return self.stops[idx]

    def get_time(self, station):
        idx = self.line.get_stations().index(station)
        return self.arrival_time[idx]
