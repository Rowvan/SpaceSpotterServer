import json, time, random

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
    
    @classmethod
    def get_status(cls, status : int):
        if status == Status.OCCUPIED:
            return "OCCUPIED"
        elif status == Status.VACANT:
            return "VACANT"
        elif status == Status.TIMED:
            return "TIMED"

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

class SpaceData:
    def __init__(self):
        self.popularity : int = 0               # times used in last 24h
        self.time_last_populated : int = 0      # time last entered
        self.time_last_vacated : int = 0        # time last exited
    
    def to_dict(self):
        return self.__dict__
    
    @classmethod
    def from_dict(cls, data : dict):
        new_data = SpaceData()
        for key in data:
            setattr(new_data, key, data[key])
        return new_data

class Space:
    """Represents a Parking Space"""
    SMALL = 0       # For small cars
    ANY = 1         # For any cars/trucks
    TRUCK = 2       # For semis
    RESERVED = 3    # For special staff or VIP
    HANDICAPPED = 4 # For handicapped

    SERVER = None
    def __init__(self):
        self.id : str = None
        self.type : int = None
        self.pos_x : float = None
        self.pos_y : float = None
        self.pos_z : float = None
        self.pos_x_r : float = None
        self.pos_y_r : float = None
        self.pos_z_r : float = None
        self.status : int = None
        self.is_metered : bool = None
        self.price : float = None
        self.popularity : int = 0
        self.time_last_populated : int = 0
        self.time_last_vacated : int = 0

        self.lot_id : str = None

    def pos(self) -> Position:
        return Position(self.pos_x, self.pos_y, self.pos_z,
                        self.pos_x_r, self.pos_y_r, self.pos_z_r)
    
    def set_pos(self, pos : Position):
        self.pos_x = pos.x
        self.pos_y = pos.y
        self.pos_z = pos.z
        self.pos_x_r = pos.x_r
        self.pos_y_r = pos.y_r
        self.pos_z_r = pos.z_r

    def get_status(self) -> str:
        if self.status == Status.OCCUPIED:
            return "OCCUPIED"
        elif self.status == Status.VACANT:
            return "VACANT"
        elif self.status == Status.TIMED:
            return "TIMED"
        
    def set_status(self, status : str):
        if status == "OCCUPIED":
            self.status = Status.OCCUPIED
        elif status == "VACANT":
            self.status = Status.VACANT
        elif status == "TIMED":
            self.status = Status.TIMED

    def space_data(self) -> SpaceData:
        new_sd = SpaceData()
        new_sd.popularity = self.popularity
        new_sd.time_last_populated = self.time_last_populated
        new_sd.time_last_vacated = self.time_last_vacated

        return new_sd

    def to_dict(self):
        return self.__dict__
    
    @classmethod
    def from_dict(cls, data : dict):
        new_space = Space()
        for key in data:
            setattr(new_space, key, data[key])
        return new_space

class Lot:
    """Represents a Parking Lot"""
    SERVER = None
    def __init__(self):
        self.pos : Position = Position()
        self.spaces : list[str] = []
        self.id : str = None

        self.inst_id : str = None

    def add_space(self, space : Space):
        self.spaces.append(space.id)
    
    def remove_space(self, space : Space):
        # print(f"removing from len {len(self.spaces)}")
        for x in range(len(self.spaces) - 1, -1, -1):
            # print(x)
            s = self.spaces[x]
            if s == space.id:
                self.spaces.pop(x)

    def get_spaces(self) -> list[Space]:
        ret = []
        for space in self.spaces:
            ret.append(self.SERVER.get_space(space))
        return ret

    def to_dict(self):
        return self.__dict__
    
    @classmethod
    def from_dict(cls, data : dict):
        new_lot = Lot()
        for key in data:
            setattr(new_lot, key, data[key])
        return new_lot

class Institution:
    """Represents an institution, such as a university or
    a company"""
    SERVER = None
    def __init__(self):
        self.lots : list[str] = []
        self.name : str = None

        self.id : int = None
        self.nickname : str = None
        self.email : str = None

        self.username : str = None
        self.password : str = None
    
    def add_lot(self, lot : Lot):
        self.lots.append(lot.id)
    
    def remove_lot(self, lot : Lot):
        for x in range(len(self.lots)):
            l = self.lots[x]
            if l == lot.id:
                self.lots.pop(x)
            
    def to_dict(self):
        return self.__dict__
    
    def get_lots(self) -> list[Lot]:
        ret = []
        for lot in self.lots:
            ret.append(self.SERVER.get_lot(lot))
        return ret
    
    @classmethod
    def from_dict(cls, data : dict):
        new_inst = Institution()
        for key in data:
            setattr(new_inst, key, data[key])
        return new_inst

'''class LotCollection:
    """Represents a collection of lots, potentially for a
    campus or several buildings under one location"""
    def __init__(self):
        self.lots : list[Lot] = []
        self.name : str = None

    def add_lot(self, lot : Lot):
        self.lots.append(lot)
    
    def remove_lot(self, lot : Lot):
        for x in range(len(self.lots)):
            l = self.lots[x]
            if l.pos.x == lot.pos.x and l.pos.y == lot.pos.y:
                self.lots.pop(x)
'''

def get_id() -> str:
    """Returns a unique id"""
    ret = ""
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ12345678901234567890"
    for x in range(10):
        ret += random.choice(chars)
    return ret

class Server:
    """Represents the server managing all the different lots"""
    def __init__(self) -> None:
        self.spaces : list[Space] = []
        self.lots : list[Lot] = []
        self.institutions : list[Institution] = []

        spaces_data = json.load(open("data\\spaces.json", "r"))
        lots_data = json.load(open("data\\lots.json", "r"))
        inst_data = json.load(open("data\\institutions.json", "r"))

        for space in spaces_data["spaces"]:
            self.spaces.append(Space.from_dict(space))
        
        for lot in lots_data["lots"]:
            self.lots.append(Lot.from_dict(lot))

        for inst in inst_data["institutions"]:
            self.institutions.append(Institution.from_dict(inst))

    def backup(self):
        """Backs up the server data"""
        spaces = {
            "spaces" : []
        }
        lots = {
            "lots" : []
        }
        insts = {
            "institutions" : []
        }

        for space in self.spaces:
            spaces["spaces"].append(space.to_dict())
        
        for lot in self.lots:
            lots["lots"].append(lot.to_dict())
        
        for inst in self.institutions:
            insts["institutions"].append(inst.to_dict())
        
        with open("data\\spaces.json", "w") as f:
            json.dump(spaces, f)
        
        with open("data\\lots.json", "w") as f:
            json.dump(lots, f)
        
        with open("data\\institutions.json", "w") as f:
            json.dump(insts, f)

    def get_space(self, id : str) -> Space:
        for space in self.spaces:
            if space.id == id:
                return space
            
    def get_lot(self, id : str) -> Lot:
        for lot in self.lots:
            if lot.id == id:
                return lot
            
    def get_institution(self, id : int) -> Institution:
        for inst in self.institutions:
            if inst.id == id:
                return inst
            
    def add_space(self, space : Space):
        space.id = get_id()
        self.spaces.append(space)
        self.get_lot(space.lot_id).spaces.append(space.id)
    
    def add_lot(self, lot : Lot):
        print(f"adding lot {self.get_institution(lot.inst_id).nickname}")
        lot.id = get_id()
        self.lots.append(lot)
        print(f"adding lot id: {lot.id}")
        self.get_institution(lot.inst_id).lots.append(lot.id)
            
    def add_institution(self, inst : Institution):
        inst.id = get_id()
        for insti in self.institutions:
            if insti.username == inst.username:
                raise ValueError("Username already exists")
        self.institutions.append(inst)
    
    def remove_space(self, space : Space):
        for x in range(len(self.spaces)):
            s = self.spaces[x]
            if s.id == space.id:
                self.spaces.pop(x)
                break
        self.get_lot(space.lot_id).remove_space(space)

    def get_full_inst(self, nickname : str) -> Institution:
        inst = self.get_institution(self.get_inst_id(nickname))

        for x in range(len(inst.lots)):
            if type(inst.lots[x]) != str:
                inst.lots[x] = inst.lots[x].id
            lot = self.get_lot(inst.lots[x])
            print(f"indx: {x}")
            print(f"lot {x}: {inst.lots[x]}")
            
            for y in range(len(lot.spaces)):
                space = self.get_space(lot.spaces[y])
                lot.spaces[y] = space
            inst.lots[x] = lot

    def inst_login_good(self, username : str, password : str) -> bool:
        for inst in self.institutions:
            if inst.username == username and inst.password == password:
                return True
        return False
    
    def get_inst_id(self, nickname : str) -> int:
        for inst in self.institutions:
            if inst.nickname == nickname:
                return inst.id
    
    def does_username_exist(self, username : str) -> bool:
        for user in self.usernames:
            if user == username:
                return True
        return False