import unittest
import os
import csv
import tempfile # os, csv, and tempfile are new

from backEndShopLyft import ClothingItem, User, UserManager, ClothingCatalogue

##############################
# Tests for ClothingItem
##############################
class TestClothingItem(unittest.TestCase):
    def setUp(self):
        self.item = ClothingItem("TShirt", "M", "Red", "Unisex", 19.99, 10, "Nike")
    
    def test_str(self):
        expected = ("Name: TShirt, Size: M, Colour: Red, Gender: Unisex, Price: 19.99, "
                    "Quantity: 10, Brand: Nike, Image: ")
        self.assertEqual(str(self.item), expected)
    
    def test_to_dict(self):
        expected = {
            'name': "TShirt",
            'size': "M",
            'colour': "Red",
            'gender': "Unisex",
            'price': 19.99,
            'quantity': 10,
            'brand': "Nike",
            'image': ""
        }
        self.assertEqual(self.item.to_dict(), expected)
    
    def test_from_dict(self):
        data = {
            'name': "Jeans",
            'size': "L",
            'colour': "Blue",
            'gender': "Male",
            'price': "49.99",
            'quantity': "5",
            'brand': "Levi's",
            'image': "dummy.png"
        }
        item = ClothingItem.from_dict(data)
        self.assertEqual(item.name, "Jeans")
        self.assertEqual(item.size, "L")
        self.assertEqual(item.colour, "Blue")
        self.assertEqual(item.gender, "Male")
        self.assertEqual(item.price, 49.99)
        self.assertEqual(item.quantity, 5)
        self.assertEqual(item.brand, "Levi's")
        self.assertEqual(item.image, "dummy.png")

##############################
# Tests for UserManager
##############################
class TestUserManager(unittest.TestCase):
    def setUp(self):
        self.user_manager = UserManager()
        self.user = User("testuser", "password", "admin")
        self.user_manager.add_user(self.user)
    
    def test_add_user(self):
        initial_count = len(self.user_manager.users)
        new_user = User("newuser", "pass", "employee")
        result = self.user_manager.add_user(new_user)
        self.assertEqual(len(self.user_manager.users), initial_count + 1)
        self.assertIn("User added successfully.", result['message'])
    
    def test_login_success(self):
        result = self.user_manager.login("testuser", "password")
        self.assertIn("Welcome, testuser!", result['message'])
        self.assertEqual(result['user']['username'], "testuser")
    
    def test_login_failure(self):
        result = self.user_manager.login("wronguser", "wrongpass")
        self.assertIn("Invalid credentials", result['message'])

    # # Opaque
    # def test_invalid_login_attempts(self):
    #     result1 = self.user_manager.login("testuser", "wrongpass")
    #     result2 = self.user_manager.login("testuser", "incorrect")
    #     self.assertIn("Invalid credentials", result1['message'])
    #     self.assertIn("Invalid credentials", result2['message'])
    #     # Ensure that no user is logged in after invalid attempts.
    #     self.assertIsNone(self.user_manager.logged_in_user)

##############################
# Tests for ClothingCatalogue
##############################
class TestClothingCatalogue(unittest.TestCase):
    def setUp(self):
        # Create a temporary CSV file for testing.
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        self.filename = self.temp_file.name
        self.temp_file.close() 
        
        # Initialize catalogue with the temporary file.
        self.catalogue = ClothingCatalogue(filename=self.filename)
        self.catalogue.items = [
            ClothingItem("TShirt", "M", "Blue", "Unisex", 19.99, 10, "Nike"),
            ClothingItem("Jeans", "L", "Black", "Male", 49.99, 5, "Levi's"),
            ClothingItem("Jacket", "L", "Dark Blue", "Female", 59.99, 7, "Adidas"),
        ]
        self.catalogue.save_items()
    
    def tearDown(self):
        # Clean up the temporary file after tests.
        if os.path.exists(self.filename):
            os.remove(self.filename)
    
    def test_find_related_items(self):
        # Expectation is that searching for "blue" will return two items:
        # one with color "Blue" and one with color "Dark Blue".
        # Since the functionality isn't implemented, the test will fail.
        result = self.catalogue.find_related_items("blue")
        self.assertEqual(len(result), 2, "Expected 2 related items for search term 'blue'")

    # # Additional TB Test: Test save_items writes to a file correctly.
    # def test_save_items(self):
    #      # Add a new item.
    #     new_item = ClothingItem("Sweater", "L", "Green", "Unisex", 29.99, 3, "H&M")
    #     self.catalogue.items.append(new_item)
    #     # Save items and verify the save message.
    #     result = self.catalogue.save_items()
    #     self.assertIn("Items saved successfully.", result['message'])
        
    #     # Read the temporary file back to verify contents.
    #     with open(self.filename, mode='r') as file:
    #         reader = csv.DictReader(file)
    #         rows = list(reader)
    #     self.assertEqual(len(rows), 4)  # 3 initial items + 1 new item.
    #     # Check new item's attributes.
    #     self.assertEqual(rows[-1]['name'], "Sweater")
    #     self.assertEqual(rows[-1]['size'], "L")
    #     self.assertEqual(rows[-1]['colour'], "Green")
    #     self.assertEqual(rows[-1]['gender'], "Unisex")
    #     self.assertAlmostEqual(float(rows[-1]['price']), 29.99)
    #     self.assertEqual(int(rows[-1]['quantity']), 3)
    #     self.assertEqual(rows[-1]['brand'], "H&M")
    #     self.assertEqual(rows[-1]['image'], "")

    # # Additional OB Test: Removing a non-existent item.
    # def test_remove_nonexistent_item(self):
    #     initial_count = len(self.catalogue.items)
    #     result = self.catalogue.remove_item("NonExistentItem")
    #     # Since no item matches, the count should remain unchanged.
    #     self.assertEqual(len(self.catalogue.items), initial_count)
    #     self.assertIn("removed successfully", result['message'])

if __name__ == '__main__':
    unittest.main()
