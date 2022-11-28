# This file is used to store the information of food inside the fridge
import json 
import datetime


# Item expiration look-up-table
expire_table = {
    "apple": 30,
    "banana": 5,
    "orange": 20,
    "tomato": 10,
    "green pepper": 10,
    "broccoli": 12
}
IN = 1
OUT = -1
DATABASE = 'utils/data/database.json'


def get_direction(item_info):
    '''
    Given the item information, decide whether the item is going in or out of the fridge.
    TODO:
    We many change this implementation slightly in the real world settings according to the placement of the Pi-camera.
    '''
    if item_info[1] == 'up':
        return IN
    else:
        return OUT

def add_item(item, item_list):
    item_formated = {
        "type": item[0],
        "in_time": str(datetime.datetime.now().date()),
        "expire_dates": expire_table[item[0]],
        "level": item[1][2]
    }
    item_list.append(item_formated)


def remove_item(item, item_list):
    idx_remove = None # index of item to be removed from item_list
    date_diff = -1 # Remove the least recent item (with largest date diff)
    for idx, i in enumerate(item_list):
        # same type and same level
        if i['type'] == item[0] and i['level'] == item[1][2]:
            if (datetime.datetime.now()-datetime.datetime.strptime(i["in_time"], "%Y-%m-%d")).days > date_diff:
                idx_remove = idx
                date_diff = (datetime.datetime.now()-datetime.datetime.strptime(i["in_time"], "%Y-%m-%d")).days
    if not idx_remove is None:
        item_list.pop(idx_remove)
    

def change_items(item_list, database_path=DATABASE):
    '''
    Add new items detected by the `Video Analysis Module` to out database.
    '''
    with open(database_path, "r") as fp:
        print("Load the previous database")
        data = json.load(fp)

    for item in item_list:
        item_info = item[1]
        direction = get_direction(item_info)
        if direction == IN:
            add_item(item, data)
        else:
            remove_item(item, data)
    with open(database_path, "w") as fp:
        json.dump(data, fp)
        print("Save the updated item lists back to the database")
        

# Test code 1 -- add/remove items to/from the database:
# item_list = [
#     ('banana', ('right', 'up', 1)),
#     ('orange', ('right', 'up', 2)),
#     ('apple',  ('right', 'up', 1)),
#     ('banana', ('right', 'up', 1))
# ]

# change_items(item_list)


def daily_check(database_path=DATABASE):
    '''
    This part of code runs once per day to check items that are near their estimated expiration date
    Return value: reminder list - a dictionary with the level as the key, and the list of items near the expiration date as the value
    e.g. {
        1: ["apple", "banana"],
        3: ["apple", "orange"]
    }
    '''
    reminder_list = {}
    with open(database_path, "r") as fp:
        data = json.load(fp)
    for item in data:
        if (datetime.datetime.now()-datetime.datetime.strptime(item["in_time"], "%Y-%m-%d")).days / item["expire_dates"] >= 0.8:
            if item["level"] in reminder_list:
                reminder_list[item["level"]].append(item["type"])
            else:
                reminder_list[item["level"]] = [item["type"]]
    return reminder_list


# Test code 2 --- check the reminder list
# print(daily_check())


def check_with_sensor_data(sensor_data, database_path=DATABASE):
    reminder_list = {}
    with open(database_path, "r") as fp:
        data = json.load(fp)
    # TODO: combine the sensor_data and data to generate reminder_list
    return reminder_list