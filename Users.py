from Railways import Line
from Railways import Train


class Person:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def check_user_pass(self, input_username, input_password):
        if input_username == self.username and input_password == self.password:
            print("Hi")
        else:
            print("Wrong username ya password.")

    def set_user_pass(self):
        pass


class Admin(Person):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.employee_list = []

    def add_employee(self, name, email, username, password):
        new_employee = Employee(username, password)
        new_employee.name = name
        new_employee.email = email
        self.employee_list.append(new_employee)
        print("The employee is added.")
        return new_employee

    def remove_employee(self, username):
        for employee in self.employee_list:
            if employee.username == username:
                self.employee_list.remove(employee)
                print(f"{username} is removed")
                return employee
        else:
            print("There is no employee with this username.")
            return None

    def check_employee_list(self):
        if not self.employee_list:
            print("There are no employees.")
        else:
            print("employee list:")
            for employee in self.employee_list:
                print(f"name: {employee.name}, email: {
                      employee.email}, username: {employee.username}")
    # def income(self):
    #   pass


class Employee(Person):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.name = None
        self.email = None
        self.line_list = []
        self.trains = []

    def add_line(self, name, origin, destination, num_stations, stations, distance_of_stations):
        new_line = Line(name, origin, destination,
                        num_stations, stations, distance_of_stations)
        self.line_list.append(new_line)
        print(f"The line with the name '{new_line.name}' is added.")
        return new_line

    def update_line(self, line):
        print(line.info())
        # parameter = input("which one do you want to change?")
        # new_value = input()
        # for i in line.info():
        #   if parameter == i :
        #       line.info()[i] = new_value

    def remove_line(self, line_name):
        for line in self.line_list:
            if line.name == line_name:
                print(f"{line.name} is removed.")
                self.line_list.remove(line)
                return line

        print("There is no Line with this name!!\nTry again.")
        return None

    def add_train(self, id, name, line: Line, velocity, stops, stars, ticket_price, route_capacity, departure_time, *args, **kwargs):
        new_train = Train(id, name, line, velocity, stops,
                          stars, ticket_price, route_capacity, departure_time)
        self.trains.append(new_train)
        return new_train

    def remove_train(self, train_name):
        for train in self.trains:
            if train.name == train_name or train.id == train_name:
                self.trains.remove(train)
                return train
        print("There is no Train with this name or Id!!\nTry again.")
        return None

    def check_train_list(self):
        if not self.trains:
            print("There are no trains.")
        else:
            print("These are the Trains available:")
            for train in self.trains:
                print(f"Id: {train['id']}")
                print(f"Name: {train['name']}")
                print(f"Line: {train['line']}")
                print(f"Average speed: {train['avg_speed']} km/h")
                print(f"Number of stations: {train['station']}")
                for i, stop_time in enumerate(train['stop_times']):
                    print(f"Station {i+1} {stop_time} minutes")
                print(f"Stars: {train['quality']}")
                print(f"Price: {train['ticket_price']} $")
                print(f"Capacity {train['capacity']} nafar")
                print("-------")


class Costumer(Person):
    def __init__(self, name, email, username, password):
        super().__init__(username, password)
        self.name = name
        self.email = email
        self.wallet = None
        # self.total_price = 0
        self.cart = []
        # in main() we have to create a list of costumers and then check if they are new or not
        # checking if the password is strong enough

    def info(self):
        if self.wallet == None:
            wal = "not created yet"
        else:
            wal = "created before"
        return f"name: {self.name}\nusername: {self.username}\nemail address: {self.email}\nwallet: {wal}\n"

    def set_name(self, new_name):
        self.name = new_name

    def set_email(self, new_email):
        self.email = new_email

    def set_username(self, new_username):
        self.username = new_username

    def set_password(self, new_password):
        self.password = new_password

    def creating_wallet(self, creditcard_id, creditcard_password):
        self.wallet = Wallet(self, creditcard_id, creditcard_password)
        print("Your Wallet is created.")

    def delete_wallet(self):
        self.wallet = None

    def is_wallet_created(self):
        return self.wallet != None

    def get_wallet(self):
        return self.wallet

    def add_to_cart(self, train: Train, list_of_passengers):
        # self.total_price += train.passengers * train.ticket_price
        self.cart.append({'train': train.costumer_info(),
                         'passengers': list_of_passengers})

    def get_cart(self):
        return self.cart

    def purchase(self, amount):
        return self.wallet.withdraw(amount)
    '''
    def purchase(self, given_password):
        print((i for i in self.cart), end="\n")
        if self.wallet:
            self.wallet.withdraw(self.total_price, given_password)
        else:
            print("Ebteda yek Kif-e Pool besazid.")
    '''
    # def edit_purchase(self):
    #     pass
    # def refund(self):
    #     pass
    #     based on the date

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email


class Wallet:
    def __init__(self, owner, creditcard_id, creditcard_password):
        self.owner = owner
        self.creditcard_id = creditcard_id
        self.creditcard_password = creditcard_password
        self.balance = 0

    def info(self):
        return f"creditcard id: {self.creditcard_id}, balance: {self.balance}"

    def check_creditcard_id(self, id):
        return self.creditcard_id == id

    def check_creditcard_password(self, password):
        return self.creditcard_password == password

    def deposite(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient Funds"
        else:
            self.balance -= amount
            return "Payment is done."
        '''
        if given_password == self.creditcard_password and  amount <= self.balance:
            self.balance -= amount
        elif given_password == self.creditcard_password and amount > self.balance:
            print("Mojoodi kafi nist.")
        else:
            print("Ramz eshtebah ast. Dobare talash konid.")
        '''


class Passenger:
    def __init__(self, name, passport_number, age):
        self.name = name
        self.passport_number = passport_number
        self.age = age

    def __str__(self):
        return f"name: {self.name}, passport_number: {self.passport_number}, age: {self.age}"

    def info(self):
        return f"name: {self.name}, passport_number: {self.passport_number}, age: {self.age}"
