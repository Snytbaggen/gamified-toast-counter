import json

try:
    with open("data.json") as f:
        data = f.read()
        users = json.loads(data)
except:
    print("Failed to load data")
    users = {}

def calculate_top():
    global top_users
    stats = []
    for u in users.values():
        if u["name"] != "Lisse Spexlund":
            stats.append((u["toasts"], u["name"]))
    stats.sort(reverse=True)
    top_users = list(map(lambda x: str(x[0]) + " - " + x[1], stats[:3]))

current_user = None
total_toast = 0
lisse_toasts = 0
top_users = []
calculate_top()

for u in users.values():
    total_toast += u["toasts"]
    if u["name"] == "Lisse Spexlund":
        lisse_toasts += u["toasts"]

def increment_toast():
    global current_user, total_toast, lisse_toasts
    if current_user == None:
        return
    current_user["toasts"] += 1
    total_toast += 1
    if current_user["name"] == "Lisse Spexlund":
        lisse_toasts += 1
    update_user(current_user)
    calculate_top()

def logout():
    global current_user
    current_user = None

def login_user(userId) -> bool:
    global current_user
    if current_user != None and current_user["userId"] == userId:
        return False

    if userId in users:
        current_user = users[userId]
        return True
    return False

def update_user(user):
    users[user["userId"]] = user
    with open("data.json", "+w") as f:
        f.write(json.dumps(users))

def id_exists(userId):
    return userId in users

def name_exists(name):
    for u in users.values():
        if u["name"] == name:
            return True
    return False

def create_user(userId, name):
    global current_user
    new_user = {
        "userId": userId,
        "name": name,
        "toasts": 0,
        "toastDates": []
    }
    users[userId] = new_user
    current_user = new_user
    update_user(new_user)
