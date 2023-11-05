from flask import Flask, render_template, request, redirect, url_for, flash
import requests, socket

from structures import *

app = Flask(__name__)

MAX_REQ_PER_SEC_BY_IP = 50

request_list = []

database = Server()
Institution.SERVER = database
Lot.SERVER = database
Space.SERVER = database

'''
space1 = Space()
space1.id = 0
space1.type = Space.ANY
space1.pos = Position(1, 1, 1)
status1 = Status()
status1.status = Status.OCCUPIED
status1.time_next_avaliable = 0
status1.time_next_unavaliable = 0
space1.status = status1
space1.is_metered = False

space2 = Space()
space2.id = 1
space2.type = Space.ANY
space2.pos = Position(-1, -1, -1)
status2 = Status()
status2.status = Status.VACANT
status2.time_next_avaliable = 0
status2.time_next_unavaliable = 0
space2.status = status2
space2.is_metered = False

space3 = Space()
space3.id = 2
space3.type = Space.ANY
space3.pos = Position(4, 4, 4)
status3 = Status()
status3.status = Status.VACANT
status3.time_next_avaliable = 0
status3.time_next_unavaliable = 0
space3.status = status3
space3.is_metered = False

lot1 = Lot()
lot1.id = 0
lot1.pos = Position(10392, 39203, 203)
for x in range(255):
    lot1.add_space(space1)
lot1.username = "YCPAdmin"
lot1.password = "changeme7"

lot2 = Lot()
lot2.id = 1
lot2.pos = Position(56557, 34, 234)
for x in range(255):
    lot2.add_space(space1)
lot2.username = "YCPAdmin"
lot2.password = "changeme7"
'''

inst1 = Institution()
inst1.id = 0
inst1.nickname = "YCP_Hacks_2023"
inst1.username = "YCPAdmin"
inst1.password = "changeme7"

inst2 = Institution()
inst2.id = 1
inst2.nickname = "BWI_Airport"
inst2.username = "root~57"
inst2.password = "hashman-&&-90"

inst3 = Institution()
inst3.id = 2
inst3.nickname = "GA-Walmart-502"
inst3.username = "walmartPriv"
inst3.password = "targetFknSucks"

inst4 = Institution()
inst4.id = 3
inst4.nickname = "York_City_Downtown_Parking"
inst4.username = "yorkCityDT"
inst4.password = "cheeseballs" # "N6*65r3H)hfe92"

database.add_institution(inst1)
database.add_institution(inst2)
database.add_institution(inst3)
database.add_institution(inst4)

print("Institutions:")
for x in range(len(database.institutions)):
    print(f"{x}: {database.institutions[x].nickname}")

# database.new_lot(lot1)
# database.new_lot(lot2)

hostname = socket.gethostname()
app_ip = socket.gethostbyname(hostname)
home_ip = "127.0.0.1"

ALLOWED_IPS = ["10.64.136.107", home_ip, app_ip]

@app.before_request
def check_ip():
    if request.authorization is not None and request.authorization.username == "SpaceSpotterAdmin" and request.authorization.password == "changeme" and request.remote_addr not in ALLOWED_IPS:
        ALLOWED_IPS.append(request.remote_addr)
        return "Logged In", 200
    client_ip = request.remote_addr
    if client_ip not in ALLOWED_IPS:
        return "Access Denied, please login to access", 403
    
    requests_in_last_second = 0

    for x in range(len(request_list) - 1, 0, -1):
        if time.time() - request_list[x]["time"] > 2.0:
            request_list.pop(x)
            continue

    for req in request_list:
        if req["ip"] == request.remote_addr and time.time() - req["time"] <= 1.0:
            requests_in_last_second += 1

    #print(f"Requests in last second: {requests_in_last_second}")
    
    if requests_in_last_second > MAX_REQ_PER_SEC_BY_IP:
        # print("###############################################################################")
        return f"Too many requests. {MAX_REQ_PER_SEC_BY_IP}/sec max", 429

    request_list.append({
        "ip": request.remote_addr,
        "time": time.time()
    })

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/institutions")
def institutions():
    return render_template('institutions.html', institutions=database.institutions)

def institution_route(nickname):
    def decorator():
        institution = database.get_institution(database.get_inst_id(nickname))  # Replace with your actual logic
        # print(f"WAWAWAWAWAWA {institution.nickname}")
        return render_template(f"{institution.nickname}.html", institution = institution, database = database)
    return decorator

# Loop through your database and create routes
for inst in database.institutions:
    route_path = f"/parking_info/{inst.nickname}"
    endpoint_function = f"institution_{inst.nickname}"
    app.route(route_path, endpoint=endpoint_function)(institution_route(inst.nickname))

@app.route("/api")
def api():
    return render_template('api.html')

@app.route("/api/get")
def api_get():
    return render_template('api_get.html')

@app.route("/api/get/lot", methods=['POST'])
def lot():
    if request.authorization is None or not database.inst_login_good(request.authorization.username, request.authorization.password):
        return "Unauthorized", 401
    inst_id = request.json.get('IID')
    lot_id = request.json.get('LOTID')  # Using request.json to access JSON data

    inst : Institution = None
    try:
        inst = database.institutions[inst_id]
    except:
        return "Institution not found", 404
    if inst is None:
        return "Institution not found", 404
    
    lot : Lot = None
    try:
        lot = database.get_lot(inst.lots[lot_id])
    except:
        return "Lot not found", 404
    if lot is None or lot.inst_id != inst.id:
        return "Lot not found", 404
    return lot.to_dict()

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/demo")
def demo():
    return render_template('demo.html')

@app.route("/demos")
def demos():
    return redirect(url_for("demo"))

@app.route("/api/get/lot/status", methods=['POST'])
def get_lot_status():
    if request.authorization is None or not database.inst_login_good(request.authorization.username, request.authorization.password):
        return "Unauthorized", 401
    
    inst_id = request.json.get('IID')

    inst : Institution = None
    try:
        inst = database.institutions[inst_id]
    except:
        return "Institution not found", 404
    if inst is None:
        return "Institution not found", 404

    lot_id = request.json.get('LOTID')
    lot : Lot = None
    try:
        lot = database.get_lot(inst.lots[lot_id])
    except:
        return "Lot not found", 404
    if lot is None or lot.inst_id != inst.id:
        return "Lot not found", 404
    
    statuses = []
    
    for space in lot.spaces:
        statuses.append(database.get_space(space).status)
    
    return { "statuses": statuses }

@app.route("/api/get/space", methods=['POST'])
def space():
    if request.authorization is None or not database.inst_login_good(request.authorization.username, request.authorization.password):
        print(f"Username: '{request.authorization.username}'\nPassword: '{request.authorization.password}'")
        return "Unauthorized, invalid authorization", 401
    
    inst_id = request.json.get('IID')
    lot_id = request.json.get('LOTID')  # Using request.json to access JSON data
    
    space_id = request.json.get('SPACEID')

    inst : Institution = None

    try:
        inst = database.institutions[inst_id]
    except:
        return "Institution not found", 404
    if inst is None:
        return "Institution not found", 404

    lot : Lot = None
    try:
        lot = database.get_lot(inst.lots[lot_id])
    except:
        return "Lot not found", 404
    
    if lot is None or lot.inst_id != inst.id:
        return "Lot not found", 404

    space : Space = None
    try:
        space = database.get_space(lot.spaces[space_id])
    except:
        return "Space not found", 404
    if space is None or space.lot_id != lot.id:
        return "Space not found", 404

    return space.to_dict()

@app.route("/api/get/institution", methods=['POST'])
def institution():
    if request.authorization is None or not database.inst_login_good(request.authorization.username, request.authorization.password):
        return "Unauthorized, invalid authorization", 401
    institution_id = request.json.get("IID")

    inst : Institution = None
    try:
        inst = database.institutions[institution_id]
    except:
        return "Institution not found", 404

    if inst is None:
        return "Institution not found", 404

    return inst.to_dict()

@app.route("/login")
def user_login_page():
    return render_template("login.html")

@app.route("/api/update/space", methods=["POST"])
def update_space():
    if request.authorization is None or not database.inst_login_good(request.authorization.username, request.authorization.password):
        # print(f"Username: '{request.authorization.username}'\nPassword: '{request.authorization.password}'")
        # print(len(request.authorization.password))
        # print(len(lot1.password))
        print(f"Username: '{request.authorization.username}'\nPassword: '{request.authorization.password}'")
        return "Unauthorized, invalid authorization", 401

    data : bytes = request.get_data()

    # print(data)

    try:
        data : dict = json.loads(data)
    except:
        return "Invalid JSON", 400

    inst : Institution = None
    try:
        inst = database.institutions[data["IID"]]
    except:
        return "Institution not found", 404

    if inst is None:
        return "Institution not found", 404
    
    lot : Lot = None
    try:
        lot = database.get_lot(inst.lots[data["LOTID"]])
    except:
        return "Lot not found", 404

    if lot is None:
        return "Lot not found", 404
    
    status = Status()
    status.status = Status.OCCUPIED if data["STATUS"] == 1 else Status.VACANT

    space : Space = None
    try:
        space = database.get_space(lot.spaces[data["SPACEID"]])
    except:
        return "Space not found", 404

    if space is None:
        return "Space not found", 404

    space.status = status.status
    # print(f"Updated space {data['SPACEID']} to {Status.get_status(status.status)}")
    return "OK", 200

@app.route("/login/submit", methods=["POST"])
def user_login_submit():
    username = request.form.get("username")
    password = request.form.get("password")
    if database.inst_login_good(username, password):
        return redirect(url_for("institutions"))
    else:
        flash("Invalid username or password")
        return redirect(url_for("user_login_page"))

@app.route("/api/update/lot", methods=["POST"])
def update_lot():
    if (request.authorization is None or
        not database.inst_login_good(
            request.authorization.username,
            request.authorization.password)
    ):
        #print(f"Username: '{request.authorization.username}'\nPassword: '{request.authorization.password}'")
        return "Unauthorized, invalid authorization", 401

    data : bytes = request.get_data()

    #print(f"DB: {len(database.lots)}")
    #print(f"Data: {data}")

    #print(data)

    try:
        data : dict = json.loads(data)
    except:
        return "Invalid JSON", 400
    
    inst : Institution = None
    try:
        inst = database.institutions[data["IID"]]
    except:
        return "Institution not found", 404

    if inst is None:
        return "Institution not found", 404

    lot_id = data["LOTID"]

    #print(f"DB ({inst.nickname}): {len(inst.lots)}")
    #print(f"Data: {lot_id}")

    lot : Lot = None
    try:
        lot = database.get_lot(inst.lots[lot_id])
    except:
        return "Lot not found", 404

    if lot == None:
        return "Lot not found", 404
    
    if len(lot.spaces) != len(data["SPACES"]):
        return f"Invalid data, lot {lot.id} has {len(lot.spaces)} spaces, not {len(data['SPACES'])}", 400

    for space_id in lot.spaces:
        #print(f"Len: {len(lot.spaces)}\nDB: {len(database.spaces)}")
        #print(f"Removing space {space_id} from lot {lot.id}")
        space = database.get_space(space_id)
        database.remove_space(space)
    lot.spaces.clear()

    for x in range(len(data["SPACES"])):
        _space = Space()
        _space.id = x
        _space.type = Space.ANY
        _space.lot_id = lot.id
        _space.set_pos(Position(0, 0, 0))
        _space.status = Status.OCCUPIED if data["SPACES"][x] == 1 else Status.VACANT
        _space.is_metered = False
        database.add_space(_space)

    #print(f"Lot {lot_id} {database.get_institution(lot.inst_id).nickname} updated/booted")
    
    return "OK", 200
        
@app.route("/api/new/lot", methods=["POST"])
def mk_new_lot():
    if (request.authorization is None or
        not database.inst_login_good(
            request.authorization.username,
            request.authorization.password)
    ):
        print(f"Username: '{request.authorization.username}'\nPassword: '{request.authorization.password}'")
        return "Unauthorized, invalid authorization", 401
    
    data : bytes = request.get_data()

    #print(data)

    try:
        data : dict = json.loads(data)
    except:
        return "Invalid JSON", 400

    inst_id = data["IID"]
    lot_id = data["LOTID"]

    inst : Institution = None
    try:
        inst = database.institutions[inst_id]
    except:
        return "Institution not found", 404
     
    if inst is None:
        return "Institution not found", 404
    
    lot : Lot = None
    try:
        lot = database.get_lot(inst.lots[lot_id])
    except:
        pass

    if lot is not None:
        return f"Invalid json, Lot {lot.id} already exists. next lot id is {len(inst.lots)}", 400

    new_lot = Lot()
    new_lot.pos = Position(0, 0, 0)
    new_lot.inst_id = inst.id
    
    database.add_lot(new_lot)
    
    for x in range(len(data["SPACES"])): 
        _space = Space()
        _space.id = x
        _space.type = Space.ANY
        _space.status = Status.OCCUPIED if data["SPACES"][x] == 1 else Status.VACANT
        _space.lot_id = new_lot.id
        database.add_space(_space)

    print(f"Lot {lot_id} added to {inst.nickname} with {len(data['SPACES'])} spaces")
    return "OK", 200

app.run(host = "0.0.0.0", port = 80)