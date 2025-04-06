import getpass
import csv
import os
from collections import Counter

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
    
    def __init__(self, filename="catalogue.csv", image_folder="static/images"):  #default path set here/ last time it wasnt like this
        self.filename = filename
        self.image_folder = image_folder
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
        try:
            if not os.path.exists(self.image_folder):
                print(f"Warning: Image folder not found at {self.image_folder}")
                return

            image_files = sorted(
                [f for f in os.listdir(self.image_folder)
                if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            )

            for i, item in enumerate(self.items):
                if not item.image and i < len(image_files):
                    #should work on the web with this
                    item.image = f"{self.image_folder.replace(os.sep, '/')}/{image_files[i]}"
        except Exception as e:
            print(f"Image assignment error: {e}")



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
        if attribute in ['size', 'colour', 'gender', 'price', 'brand', 'quantity']: # Added quantity sorting - Jayden
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

        """
        inputs should look like the one sent on discord: 

        filters = {"brand": ["Gucci", "polo"], "size": ['small', 'medium'], "price":[0,60]}
        filtered = catalogue.get_filtered_items(filters)

        I left filter by price in the code cause it still has the greater than and less than feature,
        just don't use it if it breaks the system

        """

        if not self.items:
            return {'message': "No items in catalogue.", 'filtered_items': []}

        filtered_items = self.items
        
        for key, values in filters.items():
            if not values:
                continue
            
            if key == "price":
                if isinstance(values, list) and len(values) == 2:
                    try:
                        lower_bound = float(values[0])
                        upper_bound = float(values[1])
                        filtered_items = [
                            item for item in filtered_items
                            if lower_bound <= item.price <= upper_bound
                        ]
                    except (ValueError, TypeError):
                        continue
                continue
            
            if not isinstance(values, list):
                values = [values]
            
            values = [str(value).strip().lower() for value in values if value and str(value).strip()]
            
            if hasattr(self.items[0], key):  # Check if the attribute exists
                filtered_items = [
                    item for item in filtered_items
                    if getattr(item, key, "").strip().lower() in values
                ]
        
        return {'filtered_items': [item.to_dict() for item in filtered_items]}
    
    def find_related_items(self, search_term):

        """
        should find items related to the specified item based on shared attributes, found people doing something similar here

        https://stackoverflow.com/questions/8866011/the-approach-to-calculating-similar-objects-based-on-certain-weighted-criteria
        https://stackoverflow.com/questions/16720549/calculating-a-weighted-similarity
    
        things to put in:
            item_name (str): name of the item to find related items for
            
        returns:
            dictionairy: contains message and list of related items
        """
        
        if not search_term or not isinstance(search_term, str):
            return {'message': "Invalid search term.", 'related_items': []}
        
        search_lower = search_term.strip().lower()
        related_items = []
        
        for item in self.items:
            # count matches based on attributes
            match_score = 0
            
            if search_lower in item.name.lower():
                match_score += 3  #higher weight for name match
            if search_lower in item.brand.lower():
                match_score += 2  # brand is also important
            if search_lower in item.colour.lower():
                match_score += 1
            if search_lower in item.size.lower():
                match_score += 1
            if search_lower in item.gender.lower():
                match_score += 1
            
            if match_score > 0:
                related_items.append((match_score, item))
        
        # Sort by match score in descending order
        related_items.sort(reverse=True, key=lambda x: x[0])
        
        return {
            'message': f"Found {len(related_items)} related items.",
            'related_items': [item.to_dict() for _, item in related_items]
        }


    def filter_by_price(self, lower_bound, upper_bound):

        """
        example usage:
        # Filtering by price
            
            lower_bound = 10.0
            upper_bound = 20.0
            result = store.filter_by_price(lower_bound, upper_bound)
            
            print("Items within price range:")
            for item in result['items_within_range']:
                print(item)
            
            print("Items below price range:")
            for item in result['items_below_range']:
                print(item)
            
            print("Items above price range:")
            for item in result['items_above_range']:
                print(item)

            call whichever one of the three dictionaries you want to get the results
        """
        
        if not self.items:
            return {'message': "No items in catalogue.", 'items_within_range': [], 'items_below_range': [], 'items_above_range': []}
        
        items_within_range = []
        items_below_range = []
        items_above_range = []
        
        for item in self.items:
            if lower_bound <= item.price <= upper_bound:
                items_within_range.append(item)
            elif item.price < lower_bound:
                items_below_range.append(item)
            else:
                items_above_range.append(item)
        
        return {
            'items_within_range': [item.to_dict() for item in items_within_range],
            'items_below_range': [item.to_dict() for item in items_below_range],
            'items_above_range': [item.to_dict() for item in items_above_range]
        }

    def search_items(self, search_string):

        """
        example usage:

        results = store.search_items("Sus")
    
        for item in results['matching_items']:
            print(item)

        should list the item that has "Sus" as one of its attributes, works for any string i think

        """
       
        if not search_string or not isinstance(search_string, str):
            return {'message': "Invalid search string.", 'matching_items': []}
        
        if not self.items:
            return {'message': "No items in catalogue.", 'matching_items': []}
        
        search_lower = search_string.strip().lower()
        matching_items = []
        
        for item in self.items:
            if (search_lower in item.name.lower() or
                search_lower in item.size.lower() or
                search_lower in item.colour.lower() or
                search_lower in item.gender.lower() or
                search_lower in item.brand.lower() or
                search_lower in item.image.lower() or
                search_lower in str(item.price).lower() or
                search_lower in str(item.quantity).lower()):
                matching_items.append(item)
        
        return {
            'message': f"Found {len(matching_items)} matching items.",
            'matching_items': [item.to_dict() for item in matching_items]
        }

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
        #catalogue now automatically uses static/images
        self.catalogue = ClothingCatalogue(image_folder="static/images")
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
    
    def filter_by_price(self, lower_bound, upper_bound):
        return self.catalogue.filter_by_price(lower_bound, upper_bound)

    def search_items(self, search_string):
        return self.catalogue.search_items(search_string)
    
    def find_related_items(self, item_name):
        return self.catalogue.find_related_items(item_name)
