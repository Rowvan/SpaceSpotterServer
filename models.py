import json

class Position:
    """Represents a 3D coordinate with orientation
    The coordinate system is as follows:
    x, y, and z are either long/lat or relational IN METERS
    to a long/lat coordinate. z coordinate is the height from sea level"""
    LONG_LAT = 0
    RELATIONAL = 1
    def __init__(self, x : float = 0, y : float = 0, z : float = 0,
                 x_r : float = 0, y_r : float = 0, z_r : float = 0):
        self.x : float = x      # x-cor
        self.y : float = y      # y-cor
        self.z : float = z      # z-cor

        self.x_r : float = x_r  # rotation upon x-axis
        self.y_r : float = y_r  # rotation upon y-axis
        self.z_r : float = z_r  # rotation upon z-axis

        self.type : int         # Type of position,
                                #  is it long/lat or relational

    
    def to_dict(self):
        return self.__dict__
    
    @classmethod
    def from_dict(cls, data : dict):
        new_pos = Position()
        for key in data:
            setattr(new_pos, key, data[key])
        return new_pos

class Status:
    """Represents the status of a parking space"""
    OCCUPIED = 0
    VACANT = 1
    TIMED = 2
    def __init__(self):
        self.status : int = None
        self.time_next_avaliable : int = None
        self.time_next_unavaliable : int = None
    
    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data : dict):
        new_status = Status()
        for key in data:
            setattr(new_status, key, data[key])
        return new_status

class Space:
    """Represents a Parking Space"""
    SMALL = 0       # For small cars
    ANY = 1         # For any cars/trucks
    TRUCK = 2       # For semis
    RESERVED = 3    # For special staff or VIP
    HANDICAPPED = 4 # For handicapped
    def __init__(self):
        self.id : int = None
        self.type : int = None
        self.pos : Position = None
        self.status : Status = None
        self.is_metered : bool = None
        self.price : float = None
    
    def to_dict(self):
        data = self.__dict__
        data["pos"] = self.pos.to_dict()
        data["status"] = self.status.to_dict()
        return data
    
    @classmethod
    def from_json(cls, data : dict):
        new_space = Space()
        new_space.id = data["id"]
        new_space.type = data["type"]
        new_space.pos = Position.from_dict(data["pos"])
        new_space.status = Status.from_dict(data["status"])
        new_space.is_metered = data["is_metered"]
        new_space.price = data["price"]
        return new_space
    
    def get_color(self):
        return 'green' if self.status.status == Status.VACANT else 'red'

class Lot:
    """Represents a Parking Lot"""
    def __init__(self):
        self.pos : Position = Position()
        self.spaces : list[Space] = []
        self.id : int = None

        self.username : str = None
        self.password : str = None

    def add_space(self, space : Space):
        self.spaces.append(space)
    
    def remove_space(self, space : Space):
        for x in range(len(self.spaces)):
            s = self.spaces[x]

    
class ParkingLotStatus:
    def __init__(self, is_occupied):
        self.is_occupied = is_occupied


    def get_color(self):
        return 'green' if self.is_occupied else 'red'
    
