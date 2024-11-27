import time
import regex
import datetime
from Users import Person
from Users import Admin
from Users import Employee
from Users import Costumer
from Users import Wallet
from Users import Passenger
from Railways import Line
from Railways import Train
costumers = []
employees = []
lines = []
trains = []
train_admin = Admin("SVC", "123456")


def check_time(time):
    if regex.search(r"^\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}$", time):
        if 0 <= int(time[11:13]) <= 23 and 0 <= int(time[14:16]) <= 59 and 0 <= int(time[17:]) <= 59:
            m = int(time[5:7])
            d = int(time[8:10])
            if m == 1 or m == 3 or m == 5 or m == 7 or m == 8 or m == 10 or m == 12:
                if 1 <= d <= 31:
                    return True
            elif m == 2:
                if 1 <= d <= 28:
                    return True
            elif m == 4 or m == 6 or m == 9 or m == 11:
                if 1 <= d <= 30:
                    return True
    return False


def check_email(email):
    if regex.search(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", email):
        return True
    return False


def warning(train1: Train, train2: Train):
    for station1 in train1.get_line().get_stations():
        for station2 in train2.get_line().get_stations():
            if station1 == station2:
                time1 = train1.get_time(station1)
                time2 = train2.get_time(station2)
                if time2 <= time1 <= time2 + datetime.timedelta(minutes=train2.get_stop(station2)) or time1 <= time2 <= time1 + datetime.timedelta(minutes=train1.get_stop(station1)):
                    return False
    return True


def control_panel(admin):
    print("To add a new employee enter 1")
    print("To remove an existing employee enter 2")
    print("To see a list of employees enter 3")
    print("To return to previous panel enter 0")
    print("If you want to return to your panel in any stage , please enter 0")

    choice = input("Enter your choice:")

    if choice == "1":
        name = input("Enter the name:")
        if name == "0":
            control_panel(admin)
        while not check_name(name):
            print("You must just enter alphabets and spaces. Try again")
            name = input("Enter the name: ")
            if name == '0':
                control_panel(admin)

        email = input("Enter the Email:")
        if email == "0":
            control_panel(admin)
        while not check_email(email):
            print("The entered email is invalid. Try again")
            email = input("Enter the email: ")
            if email == '0':
                control_panel(admin)
        username = input("Enter the Username:")
        if username == "0":
            control_panel(admin)
        while username == train_admin.get_username():
            print("The username is used before.")
            username = input("Enter the Username: ")
            if username == "0":
                control_panel(admin)
        for employee in employees:
            if employee.username == username or employee.email == email:
                print("Username or Email is used before.\nTry again.")
                control_panel(admin)
                break
        password = input("Enter the Password:")
        if password == "0":
            control_panel(admin)
        new_employee = admin.add_employee(name, email, username, password)
        employees.append(new_employee)
        control_panel(admin)
    elif choice == "2":
        username = input("Enter the username:")
        if username == 0:
            control_panel(admin)
        employee = admin.remove_employee(username)
        if employee:
            employees.remove(employee)
        control_panel(admin)
    elif choice == "3":
        admin.check_employee_list()
        control_panel(admin)
    elif choice == "0":
        start_menu()
    else:
        print("Not valid\nTry again")
        control_panel(admin)

def employee_panel(employee):
    code = input("To add a new line enter 1.\nTo update an existing line enter 2.\nTo remove an existing line enter 3.\nTo see the information of lines enter 4.\nTo add a new train enter 5.\nTo remove the existing train enter 6.\nTo see the information of existing trains enter 7.\nTo log out from your account enter 0.\n")
    if code == "1":
        print("If you want to return to your panel in any stage , please enter 0")
        name = input("Name:")
        if name == "0":
            employee_panel(employee)
        for i in lines:
            if name == i.name:
                print("This line already exists!!!\n Try again.")
                employee_panel(employee)
        origin = input("Origin:")
        if origin == "0":
            employee_panel(employee)
        destination = input("Destination:")
        if destination == "0":
            employee_panel(employee)
        num_stations = input("Number of Stations:")
        if num_stations == "0":
            employee_panel(employee)
        stations = []
        distance_of_stations = []
        for i in range(int(num_stations)):
            x = input(f"name of station {i+1}:")
            if x == "0":
                employee_panel(employee)
            stations.append(x)
        stations.insert(0, origin)
        stations.append(destination)
        for i in range(int(num_stations)+1):
            x = input(f"Distance of station {i} to station {i+1}:")
            if x == "0":
                employee_panel(employee)
            distance_of_stations.append(int(x))
        new_line = employee.add_line(name, origin, destination,
                                     num_stations, stations, distance_of_stations)
        lines.append(new_line)
        employee_panel(employee)
    elif code == "2":
        print("If you want to return to your panel in any stage , please enter 0")
        while True:
            x = input("Enter the name of the line:")
            if x == "0":
                employee_panel(employee)
            for line in lines:
                if x == line.name:
                    print(line.info())
                    x = line
                    break
            else:
                print("There is no line with this name!!!\nTry again.")
                continue
            y = input("Which parameter do you want to change?")
            if y == "0":
                employee_panel(employee)
            elif y == "name":
                x.set_name(input("Enter the new value:"))
            elif y == "origin":
                x.set_origin(input("Enter the new value:"))
            elif y == "destination":
                x.set_destination(input("Enter the new value:"))

            elif y == 'num_stations' or y == 'distance_of_stations' or y == 'stations':
                print("You should edit the whole stations")
                num_stations = input("Number of Stations:")
                if num_stations == "0":
                    employee_panel(employee)
                stations = []
                distance_of_stations = []
                for i in range(int(num_stations)):
                    z = input(f"name of station {i+1}:")
                    if z == "0":
                        employee_panel(employee)
                    stations.append(z)
                stations.insert(0, x.origin)
                stations.append(x.destination)
                for i in range(int(num_stations)+1):
                    z = input(f"Distance of station {i} to station {i+1}:")
                    if z == "0":
                        employee_panel(employee)
                    distance_of_stations.append(int(z))
                x.set_stations(num_stations, stations, distance_of_stations)
            else:
                print("This parameter does not exist.\nTry again")
                continue
            break
        employee_panel(employee)
    elif code == "3":
        print("If you want to return to your panel in any stage , please enter 0")
        while True:
            x = input("Enter the name of the line you want to remove:")
            if x == "0":
                employee_panel(employee)
                break
            tmp = employee.remove_line(x)
            if tmp:
                lines.remove(tmp)
                break
        employee_panel(employee)
    elif code == "4":
        for line in lines:
            print(line.info())
        while True:
            x = input("To return to your panel, please enter 0\n")
            if x == "0":
                employee_panel(employee)
                break
            else:
                print("Wrong input!!!!\nTry again")
        employee_panel(employee)
    elif code == "5":
        print("If you want to return to your panel in any stage , please enter 0")
        id = input("Id:")
        if id == "0":
            employee_panel(employee)
        name = input("Name:")
        if name == "0":
            employee_panel(employee)
        for i in trains:
            if name == i.name or id == i.id:
                print("This Train already exists!!!\nCheck Name and Id then Try again.")
                employee_panel(employee)
        line = input("Name of the Line:")
        if line == "0":
            employee_panel(employee)
        for i in lines:
            if line == i.name:
                line_obj = i
                break
        else:
            print("This line does not exist!!\nTry again")
            employee_panel(employee)
        velocity = float(input("Velocity:(km/h)"))
        if velocity == 0:
            employee_panel(employee)
        stops = []
        for i in range(int(line_obj.num_stations)):
            x = int(input(f"Stop time at station {i+1}:(min)"))
            if x == 0:
                employee_panel(employee)
            stops.append(x)
        stars = input("Stars:")
        if stars == "0":
            employee_panel(employee)
        ticket_price = int(input("Ticket Price:(dollars)"))
        if ticket_price == 0:
            employee_panel(employee)
        route_capacity = int(input("Route Capacity:"))
        if route_capacity == 0:
            employee_panel(employee)
        departure_time = input(
            "Departure Time:(please use this format : yyyy-mm-dd hh-mm-ss)")
        if departure_time == "0":
            employee_panel(employee)
        while not check_time(departure_time):
            print("You must follow the format : yyyy-mm-dd hh-mm-ss")
            departure_time = input("Departure Time: ")
            if departure_time == '0':
                employee_panel(employee)
        new_train = employee.add_train(id, name, line_obj, velocity, stops,
                                       stars, ticket_price, route_capacity, departure_time)
        for i in trains:
            if not warning(i, new_train):
                print("!!!!COLLISION WARNING!!!!\nTry changing the time.")
                employee.remove_train(new_train.name)
                break
        else:
            trains.append(new_train)
            print(f"The train with the name '{new_train.name}' is added.")
        employee_panel(employee)
    elif code == "6":
        print("If you want to return to your panel in any stage , please enter 0")
        while True:
            x = input("Enter the name or the Id of the train you want to remove:")
            if x == "0":
                employee_panel(employee)
                break
            tmp = employee.remove_train(x)
            if tmp:
                trains.remove(tmp)
                print(f"The train with name {
                      tmp.name} and Id {tmp.id} is removed.")
                break
        employee_panel(employee)
    elif code == "7":
        for train in trains:
            print(train.info())
        while True:
            x = input("To return to your panel, please enter 0\n")
            if x == "0":
                employee_panel(employee)
                break
            else:
                print("Wrong input!!!!\nTry again")
        employee_panel(employee)
    elif code == "0":
        start_menu()
    else:
        print("Wrong input.\nTry again")
        employee_panel(employee)


def payment(user: Costumer, train: Train, passengers, list_of_passengers):
    print("Whenever you want to return to your booking panel enter code 0.")
    id = input("Please enter your creditcard id: ")
    while not user.get_wallet().check_creditcard_id(id):
        if id == '0':
            break
        print("The entered id is incorrect please try again.")
        id = input("Please enter your creditcard id: ")
    if id == '0':
        booking_panel(user)
        return
    password = input("Please enter your creditcard password: ")
    while not user.get_wallet().check_creditcard_password(password):
        if password == '0':
            break
        print("The entered password is incorrect please try again.")
        password = input("Please enter your creditcard password: ")
    if password == '0':
        booking_panel(user)
        return
    print(f"Dear {user.get_name()}, the total price is {passengers*train.get_ticket_price()
                                                        }.\nFor completing the payment process please enter code 1.\nIf you want to return to the booking panel enter code 0.")
    code = input()
    while code != '0' and code != '1':
        print("The entered code is wrong please try again.")
        print(f"Dear {user.get_name()}, the total price is {passengers*train.get_ticket_price()
                                                            }.\nFor completing the payment process please enter code 1.\nIf you want to return to the booking panel enter code 0.")
        code = input()
    if code == '1':
        result = user.purchase(passengers*train.get_ticket_price())
        if result == 'Payment is done.':
            print(result)
            train.sell_tickets(passengers)
            train.add_passenger(list_of_passengers)
            user.add_to_cart(train, list_of_passengers)
            print(
                "You can see the train's information in the part called 'my ticket' in your booking panel.")
            booking_panel(user)
        else:
            print(result)
            print("You can deposite some money in your wallet in booking panel.")
            booking_panel(user)
    else:
        booking_panel(user)


def check_name(name: str):
    for char in name:
        if char != ' ' and not char.isalpha():
            return False
    return True


def get_passenger(k):
    print("Whenever you want to return to the previous page enter code 0.")
    name = input(f"please enter name of passenger {k}: ")
    if name == '0':
        return (0, 0, 0)
    if not check_name(name):
        print("The name of the passenger must just contain alphabets and spaces. Please Try Again.")
        return get_passenger(k)
    passport_number = input(f"please enter passport number of {name} : ")
    if passport_number == '0':
        return (0, 0, 0)
    age = input(f"Please enter age of {name} : ")
    if age == '0':
        return (0, 0, 0)
    if age.isdigit():
        return (name, passport_number, int(age))
    else:
        print("The age of the passenger must be a positive integer. Please Try Again.")
        return get_passenger(k)


def booking_train(user: Costumer, train: Train):
    passengers = input(
        "Please enter the number of passengers whom you want to book a seat for.\n(If you want to return to the previous page enter code 0.)\n")
    if passengers == '0':
        booking_train_panel(user)
        return
    if passengers.isdigit():
        passengers = int(passengers)
        if train.is_available(passengers):
            print(f"There are {passengers} seats available.\nThe total price for booking these seats is {
                  passengers*train.get_ticket_price()}.")
            code = input(
                "If you want to pay and finish the process of booking please enter code 1.\nIf you want to check the list of the trains again enter code 0\n")
            while (code != '0' and code != '1'):
                print("The entered code is wrong please try again.")
                code = input(
                    "If you want to pay and finish the process of booking please enter code 1.\nIf you want to check the list of the trains again enter code 0\n")
            if code == '0':
                booking_train_panel(user)
            else:
                list_of_passengers = []
                for i in range(passengers):
                    name, passport_number, age = get_passenger(i+1)
                    if name == 0:
                        booking_train(user, train)
                        return
                    list_of_passengers.append(
                        Passenger(name, passport_number, age))
                if user.is_wallet_created():
                    payment(user, train, passengers, list_of_passengers)
                else:
                    print(
                        "Please create a wallet before booking train.\nYou can see the option of creating wallet in booking panel.")
                    booking_panel(user)
        else:
            print(f"There aren't {
                  passengers} seats available for this train.\nYou can choose another train.")
            booking_train_panel(user)
    else:
        print("You must enter a number. Please Try again.")
        booking_train(user, train)


def booking_train_panel(user):
    if len(trains) == 0:
        print("There are no trains available.")
        booking_panel(user)
        return
    print("Here you can see the information of trains which are available.")
    for i in range(len(trains)):
        print(i+1, ":", trains[i].costumer_info())
    if user.get_wallet() == None:
        print("You haven't created wallet before. You can create wallet from your panel.")
        code = input("For returning to your panel enter code 0: ")
        if code == '0':
            booking_panel(user)
    code = input(f"Please enter the code of the train you want to book.\n(You must enter a number between 1 and {
                 len(trains)})\nIf you want to return to the main page of your panel please enter 0.\n")
    if code == '0':
        booking_panel(user)
        return
    if code.isdigit():
        code = int(code)
        if 1 <= code <= len(trains):
            booking_train(user, trains[int(code)-1])
        else:
            print("The entered code is wrong.")
            booking_train_panel(user)
    else:
        print("The entered code is wrong.")
        booking_train_panel(user)


def edit(user: Costumer):
    print("Whenever you want to return to previous page enter code 0.")
    info = input("Please enter the name of the info you want to change.\nIf you want to return to previous page enter code 0.\nYou must enter one of these words: name/ username/ email address/ 0\n")
    if info == 'name':
        print("In your information your name is", user.get_name())
        name = input("Please enter the new name: ")
        if name == '0':
            edit_information(user)
            return
        if not check_name(name):
            print("The name must just contains alphabets and spaces.")
            edit(user)
            return
        user.set_name(name)
        edit_information(user)
    elif info == 'username':
        print("In your information your username is", user.get_username())
        username = input("Please enter the new username: ")
        if username == '0':
            edit_information(user)
            return
        if username in [costumer.get_username() for costumer in costumers] or username == train_admin.get_username():
            print("This username is used before by another user. Please try again.")
            edit(user)
        else:
            user.set_username(username)
            edit_information(user)
    elif info == 'email address':
        print("In your information your email address is", user.get_email())
        email = input("Please enter the new email address: ")
        if email == '0':
            edit_information(user)
            return
        flag = 1
        email_of_costumers = [costumer.get_email() for costumer in costumers]
        if not check_email(email):
            flag = 0
        elif email in email_of_costumers:
            flag = -1
        while flag != 1:
            if flag == 0:
                print("The entered email address is invalid. Try again.")
            if flag == -1:
                print("The email address is used before. Try again")
            email = input("Please enter your email address: ")
            if email == '0':
                edit_information(user)
                return
            flag = 1
            if not check_email(email):
                flag = 0
            elif email in email_of_costumers:
                flag = -1
        user.set_email(email)
        edit_information(user)
    elif info == '0':
        edit_information(user)
    else:
        print("You have entered it wrong. Please try again.")
        edit(user)


def change_password(user: Costumer):
    print("Whenever you want to return to previous page enter code 0.")
    previous_password = input("Please enter your previous password: ")
    if previous_password == '0':
        edit_information(user)
    elif previous_password != user.get_password():
        print("You have entered your password incorrectly. Please try again.")
        change_password(user)
    else:
        new_password = input("Please enter the new password: ")
        if new_password == '0':
            edit_information(user)
            return
        check_password = input("Please enter it again: ")
        if check_password == '0':
            edit_information(user)
            return
        while new_password != check_password:
            print("You entered incorrectly please try again")
            new_password = input("Please enter the new password: ")
            if new_password == '0':
                edit_information(user)
                return
            check_password = input("Please enter it again: ")
            if check_password == '0':
                edit_information(user)
                return
        print("The password is changed.")
        user.set_password(new_password)
        edit_information(user)


def edit_information(user):
    print("Here you can see your information:")
    print(user.info())
    code = input("If you want to edit your information please enter code 1.\nIf you want to change your password please enter code 2.\nIf you want to return to your panel enter code 0.\n")
    if code == '1':
        edit(user)
    elif code == '2':
        change_password(user)
    elif code == '0':
        booking_panel(user)
    else:
        print("The entered code is wrong please try again.")
        edit_information(user)


def wallet(user: Costumer):
    if user.get_wallet() == None:
        code = input(
            "You haven't created wallet before.\nIf you want to creat a wallet please enter code 1.\nIf you want to return to your panel enter code 0.\n")
        if code == '0':
            booking_panel(user)
        elif code == '1':
            id = input("Please enter your creditcard id\n(If you want to return to your panel please enter code 0)\nYou must enter an id consisting of 16 digits.\n")
            if id == '0':
                booking_panel(user)
                return
            flag = False
            if id.isdigit():
                if len(id) == 16:
                    flag = True
            while not flag:
                print("Try again!")
                id = input("Please enter your creditcard id\n(If you want to return to your panel please enter code 0)\nYou must enter an id consisting of 16 digits.\n")
                if id == '0':
                    booking_panel(user)
                    return
                flag = False
                if id.isdigit():
                    if len(id) == 16:
                        flag = True
            password = input("Please enter your creditcard password\n(If you want to return to your panel please enter code 0)\nYou must enter a password consisting of 4, 5 or 6 digits.\n")
            if password == '0':
                booking_panel(user)
                return
            flag = False
            if password.isdigit():
                if 4 <= len(password) <=  6:
                    flag = True
            while not flag:
                print("Try again!")
                password = input("Please enter your creditcard password\n(If you want to return to your panel please enter code 0)\nYou must enter a password consisting of 4, 5 or 6 digits.\n")
                if password == '0':
                    booking_panel(user)
                    return
                flag = False
                if password.isdigit():
                    if 4 <= len(password) <= 6:
                        flag = True
            user.creating_wallet(id, password)
            wallet(user)
        else:
            print("The entered code is wrong.")
            wallet(user)
    else:
        print("Whenever you want to return to your booking panel enter code 0.")
        print("You have created a wallet before.\nIf you want to enter your wallet please enter code 1.\nAnd if you want to return to your booking panel enter code 0.\n")
        code = input()
        if code == '1':
            id = input("Please enter your creditcard id: ")
            if id == '0':
                booking_panel(user)
                return
            while not user.get_wallet().check_creditcard_id(id):
                print("The entered id is incorrect please try again.")
                id = input("Please enter your creditcard id: ")
                if id == '0':
                    booking_panel(user)
                    return
            password = input("Please enter your creditcard password: ")
            if password == '0':
                booking_panel(user)
                return
            while not user.get_wallet().check_creditcard_password(password):
                print("The entered password is incorrect please try again.")
                password = input("Please enter your creditcard password: ")
                if password == '0':
                    booking_panel(user)
                    return
            print(
                "You have entered your wallet.\nHere you can see your wallet's information:")
            print(user.get_wallet().info())
            code = input("If you want to delete the information of your wallet and create a new wallet please enter code 1.\nIf you want to deposite some money in your wallet please enter code 2.\nIf you want to log out from your wallet please enter code 0.\n")
            while code != '0' and code != '1' and code != '2':
                print("The entered code is wrong.")
                code = input("If you want to delete the information of your wallet and create a new wallet please enter code 1.\nIf you want to deposite some money in your wallet please enter code 2.\nIf you want to log out from your wallet please enter code 0.\n")
            if code == '1':
                user.delete_wallet()
                print("Your Wallet is deleted. Now you can create a new wallet.")
                wallet(user)
            elif code == '2':
                amount = input(
                    "Please enter the amount of money you want to deposite in your wallet(in dollars)\n(If you want to return to your panel you can enter 0)\n")
                flag = True
                if not amount.isdigit():
                    flag = False
                while not flag:
                    print("You must enter a non-negative integer.")
                    amount = input(
                        "Please enter the amount of money you want to deposite in your wallet(in dollars)\n(If you want to return to your panel you can enter 0)\n")
                    flag = True
                    if not amount.isdigit():
                        flag = False
                amount = int(amount)
                user.get_wallet().deposite(amount)
                print("Here you can see your wallet's information:")
                print(user.get_wallet().info())
                booking_panel(user)
            else:
                wallet(user)
        elif code == '0':
            booking_panel(user)
        else:
            print("You have entered a wrong code. Please try again.")
            wallet(user)


def my_tickets(user: Costumer):
    if len(user.get_cart()) == 0:
        print("There are no booked tickets.")
        booking_panel(user)
        return
    print("Here are the tickets you have booked before:")
    for idx, element in enumerate(user.get_cart()):
        print(f"{idx+1}.The train information:", element['train'])
        print("List of passengers:")
        for passenger in element['passengers']:
            print(passenger)
        print("")
    code = input("In order to return to booking panel please enter code 0: ")
    if code != '0':
        print("The entered code is wrong.")
        my_tickets(user)
    else:
        booking_panel(user)


def booking_panel(user: Costumer):
    print(f"Welcome dear {user.get_name()}")
    code = input(f"If you want to book a train please enter code 1.\nIf you want to edit your information please enter code 2.\nIf you want to work with your wallet please enter code 3.\nIf you want to go to 'My Tickets' please enter code 4.\nAnd if you want to log out please enter code 0.\n")
    if code == '1':
        booking_train_panel(user)
        # booking_panel(user)
    elif code == '2':
        edit_information(user)
    elif code == '3':
        wallet(user)
    elif code == '4':
        my_tickets(user)
    elif code == '0':
        the_user()
    else:
        print(
            'The entered code is wrong.\nYou must enter one of the codes 0, 1, 2, 3 or 4.')
        booking_panel(user)


def sign_up():
    print("Whenever you want to return to the previous page enter code 0.")
    name = input("Please enter your name: ")
    if name == '0':
        the_user()
        return
    while not check_name(name):
        name = input(
            "Please enter your name(Just alphabets and space are valid): ")
        if name == '0':
            the_user()
            return
    username = input("Please enter your username: ")
    username_of_costumers = [costumer.get_username() for costumer in costumers]
    if username == '0':
        the_user()
        return
    while username in username_of_costumers or username == train_admin.get_username():
        print("The entered username is used before. Try again")
        username = input("Please enter your username: ")
        if username == '0':
            the_user()
            return
    email_address = input("Please enter your email address: ")
    if email_address == '0':
        the_user()
        return
    flag = 1
    email_of_costumers = [costumer.get_email() for costumer in costumers]
    if not check_email(email_address):
        flag = 0
    elif email_address in email_of_costumers:
        flag = -1
    while flag != 1:
        if flag == 0:
            print("The entered email address is invalid. Try again.")
        if flag == -1:
            print("The email address is used before. Try again")
        email_address = input("Please enter your email address: ")
        if email_address == '0':
            the_user()
            return
        flag = 1
        if not check_email(email_address):
            flag = 0
        elif email_address in email_of_costumers:
            flag = -1
    password = input("Please enter a password: ")
    if password == '0':
        the_user()
        return
    check_password = input("Please enter it again: ")
    if check_password == '0':
        the_user()
        return
    while password != check_password:
        print("You entered incorrectly please try again")
        password = input("Please enter a password: ")
        if password == '0':
            the_user()
            return
        check_password = input("Please enter it again: ")
        if check_password == '0':
            the_user()
            return
    print("Your account is created dear", name)
    costumer = Costumer(name, email_address, username, password)
    costumers.append(costumer)
    the_user()
    


def log_in():
    print("Whenever you want to return to the previous page enter code 0.")
    username = input("Please enter your username: ")
    if username == '0':
        the_user()
        return
    password = input("Please enter your password: ")
    if password == '0':
        the_user()
        return
    for costumer in costumers:
        if costumer.get_username() == username:
            if costumer.get_password() == password:
                booking_panel(costumer)
            else:
                print("The entered password is incorrect. Please Try Again.")
                log_in()
            return
    print("The entered username is incorrect. Please Try again.")
    log_in()



def the_admin(admin_username, admin_password):
    print("Whenever you want to return to the start menu please enter code 0.")
    username = input("username: ")
    if username == '0':
        start_menu()
        return
    password = input("password: ")
    if password == '0':
        start_menu()
        return

    if username != admin_username or password != admin_password:
        print("Wrong username or password!!\nTry again.")
        the_admin(admin_username, admin_password)
    else:
        print("Hi Admin!\nWelcome")
        control_panel(train_admin)


def the_employee():
    username = input("Please Enter your Username :")
    password = input("Please Enter your Password :")
    for u in employees:
        if u.username == username and u.password == password:
            print(f"Welcome {username}")
            employee_panel(u)
    print("Wrong Username or Password!!\n Try again.")
    the_employee()



def the_user():
    code = input("If you haven't registered yet please sign up and enter code 1.\nIf you have registered before you can log in by entering code 2.\nFor returning to the start menu you can enter code 0.\n")
    if code == '1':
        sign_up()
    elif code == '2':
        log_in()
    elif code == '0':
        start_menu()
    else:
        print('The entered code is wrong.\nYou must enter one of the codes 0, 1 or 2.')
        the_user()


def start_menu():
    print("Welcome to SVC ticketing system.\nPlease choose your role as Admin, Employee, User.\nIf you want to exit enter code 0.")
    role = input()
    if role == 'Admin':
        the_admin(train_admin.get_username(), train_admin.get_password())
    elif role == 'Employee':
        the_employee()
    elif role == 'User':
        the_user()
    elif role == '0':
        print("Bye!!")
        exit()
    else:
        print("You must enter one of these words: Admin/Employee/User/0.\nTry Again.")
        start_menu()


start_menu()
