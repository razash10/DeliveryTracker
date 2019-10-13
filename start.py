import os
import json
from datetime import datetime


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def valid_days(num):
    try:
        if int(num) > 0:
            return True
    except ValueError:
        return False


def update_days_left():
    with open('deliveries.json', 'r') as file:
        data = json.load(file)
        for item in data["deliveries"]:
            order_date_obj = datetime.strptime(item["order_date"], "%d/%m/%y")
            time_passed = datetime.now() - order_date_obj
            days_left = int(item["estimated_days"]) - time_passed.days
            item["days_left"] = days_left

    with open('deliveries.json', 'w') as file:
        json.dump(data, file)


def whats_next_add():
    print("\nWhat's next?")
    print("1. Add another delivery")
    print("2. Print my deliveries")
    print("3. Delete an existing delivery")
    print("4. Go back to main menu")

    opt = input("\nEnter your option: ")

    options = {
        "1": "add",
        "2": "print",
        "3": "delete",
        "4": "menu",
        "5": "exit"

    }

    if opt in options:
        return options[opt]
    else:
        return "exit"


def whats_next_delete():
    print("\nWhat's next?")
    print("1. Delete another delivery")
    print("2. Print my deliveries")
    print("3. Add a new delivery")
    print("4. Back to main menu")

    opt = input("\nEnter your option: ")

    options = {
        "1": "delete",
        "2": "print",
        "3": "add",
        "4": "menu",
        "5": "exit"
    }

    if opt in options:
        return options[opt]
    else:
        return "exit"


def whats_next_print():
    print("\nWhat's next?")
    print("1. Add a new delivery")
    print("2. Delete an existing delivery")
    print("3. Go back to main menu")

    opt = input("\nEnter your option: ")

    options = {
        "1": "add",
        "2": "delete",
        "3": "menu",
        "4": "exit"
    }

    if opt in options:
        return options[opt]
    else:
        return "exit"


def main_menu():
    clear_screen()

    try:
        with open("deliveries.json", "x") as file:
            data = {"deliveries": []}
            json.dump(data, file)
    except FileExistsError:
        update_days_left()

    print("Welcome to DeliveryTracker!")
    print("What would you like to do?")
    print("1. Print my deliveries")
    print("2. Add a new delivery")
    print("3. Delete an existing delivery")
    print("4. Exit")

    opt = input("\nEnter your option: ")

    options = {
        "1": "print",
        "2": "add",
        "3": "delete",
        "4": "exit"
    }

    if opt in options:
        return options[opt]
    else:
        return "exit"


def print_deliveries():
    clear_screen()

    with open('deliveries.json', 'r') as file:
        data = json.load(file)

        if not data["deliveries"]:
            print("There is nothing to print!")
            return whats_next_print()

        print('{:<30}{:<20}{:<20}{:<20}{:<20}'.format("NAME OF ITEM", "WEBSITE",
                                                      "ORDER DATE", "ESTIMATED DAYS", "DAYS LEFT"))

        for item in data["deliveries"]:
            print('{:<30}{:<20}{:<20}{:<20}{:<20}'.format(item["name"], item["website"], item["order_date"],
                                                          str(item["estimated_days"]), str(item["days_left"])))

    return whats_next_print()


def add_delivery():
    clear_screen()

    name = input("Enter the name of the purchased item: ")

    website = input("Enter the name of the website that you bought from: ")

    order_date = input("Enter the order date in format dd/mm/yy: ")
    good_format = False
    while not good_format:
        try:
            order_date_obj = datetime.strptime(order_date, "%d/%m/%y")
            if order_date_obj:
                good_format = True
        except ValueError:
            order_date = input("Invalid input. Enter again in format dd/mm/yy: ")

    estimated_days = input("Enter estimated days to deliver: ")
    while not valid_days(estimated_days):
        estimated_days = input("Invalid number of days. Enter again: ")

    order_date_obj = datetime.strptime(order_date, "%d/%m/%y")
    time_passed = datetime.now() - order_date_obj
    days_left = int(estimated_days) - time_passed.days

    delivery = {
        "name": name,
        "website": website,
        "order_date": order_date,
        "estimated_days": int(estimated_days),
        "days_left": days_left
    }

    with open('deliveries.json', 'r') as file:
        data = json.load(file)
        data["deliveries"].append(delivery)
        sorted_data = dict(data)
        sorted_data["deliveries"] = sorted(sorted_data["deliveries"],
                                           key=lambda x: x["days_left"], reverse=False)

    with open('deliveries.json', 'w') as file:
        json.dump(sorted_data, file)
        print("\nDelivery added successfully!")

    return whats_next_add()


def delete_delivery():
    clear_screen()

    name2delete = input("Enter a desired item's name to delete: ")

    found_flag = 0

    with open('deliveries.json', 'r') as file:
        data = json.load(file)
        for delivery in data["deliveries"]:
            if delivery["name"] == name2delete:
                data["deliveries"].remove(delivery)
                found_flag = 1

    if found_flag == 0:
        print("\nDelivery wasn't found!")
    else:
        with open('deliveries.json', 'w') as file:
            json.dump(data, file)
        print("\nDelivery removed successfully!")
    return whats_next_delete()


option = "menu"

while option != "exit":
    if option == "menu":
        option = main_menu()
    elif option == "add":
        option = add_delivery()
    elif option == "delete":
        option = delete_delivery()
    elif option == "print":
        option = print_deliveries()
    else:
        option = "exit"

exit(0)
