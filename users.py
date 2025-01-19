import json

try:
    with open("data.json") as f:
        data = f.read()
        users = json.loads(data)
except:
    print("Failed to load data")
    users = {}

current_user = None
total_toast = 0

for u in users.values():
    total_toast += u["toasts"]

def increment_toast():
    global current_user, total_toast
    if current_user == None:
        return
    current_user["toasts"] += 1
    total_toast += 1
    update_user(current_user)

def logout():
    global current_user
    current_user = None

def login_user(userId) -> bool:
    global current_user
    if current_user != None and current_user["userId"] == userId:
        return False
    
    print("Trying to fetch user")
    print(users)
    print(userId)
    if userId in users:
        print("Fetching user")
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