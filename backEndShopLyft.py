import getpass
import csv
import os

class ClothingItem:
    def __init__(self, name, size, colour, gender, price, quantity, brand, image=""):
        self.name = name
        self.size = size
        self.colour = colour
        self.gender = gender
        self.price = price
        self.quantity = quantity
        self.brand = brand
        self.image = image  #attribute for images 

    def __str__(self):
        return (f"Name: {self.name}, Size: {self.size}, Colour: {self.colour}, Gender: {self.gender}, "
                f"Price: {self.price}, Quantity: {self.quantity}, Brand: {self.brand}, Image: {self.image}")

    def to_dict(self):
        return {
            'name': self.name,
            'size': self.size,
            'colour': self.colour,
            'gender': self.gender,
            'price': self.price,
            'quantity': self.quantity,
            'brand': self.brand,
            'image': self.image  # sees if image path is included
        }

    @staticmethod
    def from_dict(data):
        return ClothingItem(
            data['name'], data['size'], data['colour'], data['gender'],
            float(data['price']), int(data['quantity']), data['brand'],
            data.get('image', "")  #goes to empty if missing
        )

# catalogue that stores clothing items
class ClothingCatalogue:
    def __init__(self, filename="catalogue.csv", image_folder="images"):
        self.filename = filename
        self.image_folder = image_folder
        self.items = []
        self.load_items()

    def load_items(self):
        if not os.path.exists(self.filename):
            return {'message': f"{self.filename} not found. A new catalogue will be created."}

        with open(self.filename, mode='r') as file:
            reader = csv.DictReader(file)
            self.items = [ClothingItem.from_dict(row) for row in reader]

        self.assign_images()  #assign images if missing 

        return {'message': "Items loaded successfully.", 'items': [item.to_dict() for item in self.items]}

    def assign_images(self):
        pass
        # assigns images based on item order if not set in the csv
        # image_files = sorted([f for f in os.listdir(self.image_folder) if f.endswith(".png")])
        # for i, item in enumerate(self.items):
        #     if not item.image and i < len(image_files):
        #         item.image = os.path.join(self.image_folder, image_files[i])

    def save_items(self):
        with open(self.filename, mode='w', newline='') as file:
            fieldnames = ['name', 'size', 'colour', 'gender', 'price', 'quantity', 'brand', 'image']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for item in self.items:
                writer.writerow(item.to_dict())
        return {'message': "Items saved successfully."}

    def add_item(self, item):
        self.items.append(item)
        self.save_items()
        return {'message': "Item added successfully.", 'item': item.to_dict()}

    def remove_item(self, item_name):
        self.items = [item for item in self.items if item.name != item_name]
        self.save_items()
        return {'message': f"Item {item_name} removed successfully."}

    def edit_item(self, item_name, new_item):
        for i, item in enumerate(self.items):
            if item.name == item_name:
                self.items[i] = new_item
                self.save_items()
                return {'message': "Item edited successfully.", 'item': new_item.to_dict()}
        return {'message': "Item not found."}

    def sort_items(self, attribute):
        if attribute in ['size', 'colour', 'gender', 'price', 'brand']:
            self.items.sort(key=lambda x: getattr(x, attribute))
            self.save_items()
            return {'message': f"Items sorted by {attribute} successfully."}
        return {'message': "Invalid sorting attribute."}

    def display_items(self):
        return [item.to_dict() for item in self.items]

    def get_items_as_strings(self):
        return [
            {
                'name': str(item.name),
                'size': str(item.size),
                'colour': str(item.colour),
                'gender': str(item.gender),
                'price': str(item.price),
                'quantity': str(item.quantity),
                'brand': str(item.brand),
                'image': str(item.image)   # image is returned as a string (think this is what you wanted)
            }
            for item in self.items
        ]

    def get_filter_values(self, attribute): # modified so that brands load correctly in Staff view
        if not self.items:
            print("Catalogue is empty")
            return {'message': "No items in catalogue"}
        if not hasattr(self.items[0], attribute):
            print(f"Invalid attribute: {attribute}")
            return {'message': "Invalid atrribute"}
        unique_values = list(set(getattr(item, attribute, "").strip() for item in self.items if getattr(item, attribute, "").strip()))
        # print(f"Unique values for {attribute}: {unique_values}")  # for debugging
        return {'attribute': attribute, 'values': unique_values}

        # # should return a list of unique values for the attribute you put in
        # if not hasattr(ClothingItem, attribute):
        #     return {'message': "Invalid attribute."}

        # unique_values = list(set(getattr(item, attribute) for item in self.items))
        # return {'attribute': attribute, 'values': unique_values}

    def get_filtered_items(self, filters):
        
        # should returns a list of items matching filters you put in
        # example input: {"brand": "Levi", "size": "L"}

        filtered_items = self.items

        for key, value in filters.items():
            if hasattr(ClothingItem, key):
                filtered_items = [item for item in filtered_items if getattr(item, key) == value]

        return {'filtered_items': [item.to_dict() for item in filtered_items]}

# User and User Manager Classes
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
        return {'message': "User added successfully."}

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                self.logged_in_user = user
                return {'message': f"Welcome, {user.username}!", 'user': {'username': user.username, 'role': user.role}}
        return {'message': "Invalid credentials. Please try again."}

# admin and Employee functions
class ClothingStore:
    def __init__(self):
        self.catalogue = ClothingCatalogue()
        self.user_manager = UserManager()

    def add_item(self, name, size, colour, gender, price, quantity, brand, image=""):
        item = ClothingItem(name, size, colour, gender, price, quantity, brand, image)
        return self.catalogue.add_item(item)

    def remove_item(self, item_name):
        return self.catalogue.remove_item(item_name)

    def edit_item(self, item_name, name, size, colour, gender, price, quantity, brand, image=""):
        new_item = ClothingItem(name, size, colour, gender, price, quantity, brand, image)
        return self.catalogue.edit_item(item_name, new_item)

    def sort_items(self, attribute):
        return self.catalogue.sort_items(attribute)

    def view_items(self):
        return self.catalogue.display_items()

    def login(self, username, password):
        return self.user_manager.login(username, password)

    def get_items_as_strings(self):
        return self.catalogue.get_items_as_strings()

    def get_filter_values(self, attribute):
        return self.catalogue.get_filter_values(attribute)

    def get_filtered_items(self, filters):
        return self.catalogue.get_filtered_items(filters)
