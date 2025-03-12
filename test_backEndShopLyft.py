import unittest

# Import the classes to test from your module.
from backEndShopLyft import ClothingItem, User, UserManager

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

if __name__ == '__main__':
    unittest.main()
