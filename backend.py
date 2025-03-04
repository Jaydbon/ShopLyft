import getpass
import csv
import os

class ClothingItem:
    def __init__(self, name, size, colour, gender, price, quantity, brand):
        self.name = name
        self.size = size
        self.colour = colour
        self.gender = gender
        self.price = price
        self.quantity = quantity
        self.brand = brand

    def __str__(self):
        return f"Name: {self.name}, Size: {self.size}, Colour: {self.colour}, Gender: {self.gender}, Price: {self.price}, Quantity: {self.quantity}, Brand: {self.brand}"

    def to_dict(self):
        return {
            'name': self.name,
            'size': self.size,
            'colour': self.colour,
            'gender': self.gender,
            'price': self.price,
            'quantity': self.quantity,
            'brand': self.brand
        }

    @staticmethod
    def from_dict(data):
        return ClothingItem(data['name'], data['size'], data['colour'], data['gender'], float(data['price']), int(data['quantity']), data['brand'])

# catalogue that stores clothing items
class ClothingCatalogue:
    def __init__(self, filename="catalogue.csv"):
        self.filename = filename
        self.items = []
        self.load_items()

    def load_items(self):
        """Load items from CSV file"""
        if not os.path.exists(self.filename):
            print(f"{self.filename} not found. A new catalogue will be created.")
            return

        with open(self.filename, mode='r') as file:
            reader = csv.DictReader(file)
            self.items = [ClothingItem.from_dict(row) for row in reader]

    def save_items(self):
        """Save items to CSV file"""
        with open(self.filename, mode='w', newline='') as file:
            fieldnames = ['name', 'size', 'colour', 'gender', 'price', 'quantity', 'brand']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for item in self.items:
                writer.writerow(item.to_dict())

    def add_item(self, item):
        self.items.append(item)
        self.save_items()

    def remove_item(self, item_name):
        self.items = [item for item in self.items if item.name != item_name]
        self.save_items()

    def edit_item(self, item_name, new_item):
        for i, item in enumerate(self.items):
            if item.name == item_name:
                self.items[i] = new_item
                self.save_items()
                break

    def sort_items(self, attribute):
        if attribute == 'size':
            self.items.sort(key=lambda x: x.size)
        elif attribute == 'colour':
            self.items.sort(key=lambda x: x.colour)
        elif attribute == 'gender':
            self.items.sort(key=lambda x: x.gender)
        elif attribute == 'price':
            self.items.sort(key=lambda x: x.price)
        elif attribute == 'brand':
            self.items.sort(key=lambda x: x.brand)
        self.save_items()

    def display_items(self):
        for item in self.items:
            print(item)

#user authentication
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

class UserManager:
    def __init__(self):
        self.users = []
        self.logged_in_user = None

    def add_user(self, user):
        self.users.append(user)

    def login(self):
        username = input("Username: ")
        password = getpass.getpass("Password: ")

        for user in self.users:
            if user.username == username and user.password == password:
                self.logged_in_user = user
                print(f"Welcome, {user.username}!")
                return True
        print("Invalid credentials. Please try again.")
        return False

# admin and Employee functions
class ClothingStore:
    def __init__(self):
        self.catalogue = ClothingCatalogue()
        self.user_manager = UserManager()

    def display_menu(self):
        print("\nCatalogue Menu")
        print("1. Add Item")
        print("2. Remove Item (Admin only)")
        print("3. Edit Item (Admin only)")
        print("4. Sort Items")
        print("5. View All Items")
        print("6. Logout")

    def handle_menu(self):
        while True:
            self.display_menu()
            choice = input("Choose an option: ")

            if choice == '1':
                self.add_item()
            elif choice == '2' and self.is_admin():
                self.remove_item()
            elif choice == '3' and self.is_admin():
                self.edit_item()
            elif choice == '4':
                self.sort_items()
            elif choice == '5':
                self.view_items()
            elif choice == '6':
                self.logout()
                break
            else:
                print("Invalid choice, please try again.")

    def add_item(self):
        name = input("Enter item name: ")
        size = input("Enter item size: ")
        colour = input("Enter item colour: ")
        gender = input("Enter item gender (M/F): ")
        price = float(input("Enter item price: "))
        quantity = int(input("Enter item quantity: "))
        brand = input("Enter item brand: ")

        item = ClothingItem(name, size, colour, gender, price, quantity, brand)
        self.catalogue.add_item(item)
        print("Item added successfully.")

    def remove_item(self):
        item_name = input("Enter the name of the item to remove: ")
        item_brand = input("Enter the brand of the item to remove: ")
        self.catalogue.remove_item(item_name, item_brand)
        print("Item removed successfully.")

    def edit_item(self):
        item_name = input("Enter the name of the item to edit: ")
        name = input("Enter new item name: ")
        size = input("Enter new item size: ")
        colour = input("Enter new item colour: ")
        gender = input("Enter new item gender (M/F): ")
        price = float(input("Enter new item price: "))
        quantity = int(input("Enter new item quantity: "))
        brand = input("Enter the brand of the item: ")

        new_item = ClothingItem(name, size, colour, gender, price, quantity, brand)
        self.catalogue.edit_item(item_name, new_item)
        print("Item edited successfully.")

    def sort_items(self):
        attribute = input("Sort by (size/colour/gender/price/brand): ")
        self.catalogue.sort_items(attribute)
        print("Items sorted successfully.")

    def view_items(self):
        print("Viewing all items:")
        self.catalogue.display_items()

    def is_admin(self):
        return self.user_manager.logged_in_user and self.user_manager.logged_in_user.role == "admin"

    def logout(self):
        print(f"Goodbye, {self.user_manager.logged_in_user.username}!")
        self.user_manager.logged_in_user = None

#main Program
if __name__ == "__main__":
    #creating the store 
    store = ClothingStore()

    # add some users (admins and employees)
    admin = User(username="admin", password="admin123", role="admin")
    employee = User(username="employee", password="employee123", role="employee")

    store.user_manager.add_user(admin)
    store.user_manager.add_user(employee)

    #login
    if store.user_manager.login():
        store.handle_menu()
