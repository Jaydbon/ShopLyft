# ShopLyft Clothing Catalogue
## About the Project
**ShopLyft** is a comprehensive clothing management system that provides:
- A web-based interface for inventory management
- Role-based access control (admin and staff)
- Full creating, removing, and editing operations for clothing items (admin)
- Advanced search and filtering capabilities
- Image handling for product visualization

The system uses Flask for the web interface and Python for backend operations, with data stored in CSV format.

## Built With:
- **Flask**: A lightweight web framework for the application interface.
- **Python**: Backend logic and data processing.
- **CSV**: Data storage format for items and users.
- **Virtual Environments**: For dependency management.

## Prerequisites
- **Python 3.x** (Recommended version: 3.7 or higher)
    - Make sure python is installed on your system. You can download it from [python.org](https://www.python.org/downloads/)

## Dependencies

Core Libraries:
- **Flask**: Web application framework used to create the web application.

Standard Python Modules:
- **os**: File system operations that is used for operations such as handling file paths and directories.
- **csv**: Daa storage management that is used to read from and write to CSV files that store clothing item data and user login data. 
- **getpass**: Used to securely prompt users for passwords for login functionalities.
- **subprocess**: System command execution from within Python that is used to run commands such as activating virtual environments, installing dependencies, starting the Flask application, and running tests. 
- **sys**: System-specific parameters for interacting with the Python runtime environment that is used to handle command-line arguments and exit the script.
- **tempfile**: Temporary file handling (for testing)
- **unittest**: Testing framework

## Installation & Setup
Option 1: Manual Setup
1. Clone the repository and navigate to project directory:
    ```bash
    git clone https://github.com/Jaydbon/ShopLyft.git
    cd ShopLyft
    ```

2. Create and activate virtual environment:
    ```bash
    python -m venv venv
    # Windows:
    venv/Scripts/activate
    # macOS/Linux:
    source venv/bin/activate
    ```

3. Install dependencies and required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:
    ```bash
    python app.py
    ```

5. Open the provided URL in your web browser to access the website 

Option 2: Using Build System
1. Clone the repository and navigate to project directory:
    ```bash
    git clone https://github.com/Jaydbon/ShopLyft.git
    cd ShopLyft
    ```

2. Create and activate virtual environment:
    ```bash
    python -m venv venv
    # Windows:
    venv/Scripts/activate
    # macOS/Linux:
    source venv/bin/activate
    ```

3. Use the build system for setup:
    ```bash
    python build.py install # Installs required packages
    python build.py run # Starts application
    ```

4. Open the provided URL in your web browser to access the website (you may also run ```python build.py``` to check all commands).


## Features
### Staff Users (available to all users)
- View complete product catalogue
- Search and filter items by various attributes:
    - Name
    - Size
    - Colour
    - Gender
    - Price
    - Quantity in stock
- Sort items by various attributes:
    - Brand
    - Size
    - Gender
    - Colour
    - Price range
- View detailed product information
- Search for items by relevant terms

### Admin Users (must log in as admin to access)
- All staff privileges
- Add new products to catalogue
- Edit existing products from catalogue
- Remove existing products from catalogue (confirmation pop-up when there are 10+ items in inventory)
- Manage product images

### Implementations in Iterations
Iteration 1:
- View products and product information (Staff & Admin)
- Add new products to inventory (Admin)
- Remove existing products from catalogue (Admin)
Iteration 2:
- Edit existing products from catalogue (Admin)
- Search and filter items by various attributes (Staff & Admin):
    - Name
    - Size
    - Colour
    - Gender
    - Quantity in stock
- Sort items by various attributes (Staff & Admin):
    - Brand
    - Size
    - Gender
    - Colour
    - Price range
Iteration 3:
- Admin login (Admin)
- Search for items by relevant terms (Staff)
- Filter and/or sort items by price range (Staff & Admin)
- Implemented confirmation pop-up when 10+ items are in inventory (Admin)

## Usage Guide
### Accessing the System
1. **Login**:
    - Default admin credentials:
        - **Username**: admin[*number*]
        - **Password**: password[*number*]
        > Accepted usernames and passwords can be edited in the `adminLogins.csv`, but the default logins are set to admin/password, followed by a number

2. **Navigation**:
    - **Staff view**: Default on startup page
        - Can also be accessed from Admin page through the `Staff` button located at the top right
    - **Admin view**: Access through the `Admin` button located at the top right of the Staff Page to prompt login screen to access Admin functionalities.

### Navigating Items
Filter options are available on the left side of the webpage:
- **Sort**: Dropdown menu with available attributes (name, size, colour, gender, price, quantity) to change the order in which items are displayed.
- **Filters**: List of attributes (brand, size, gender, colour) with checkboxes for users to filter what items are displayed.
- **Price range**: Items can be filtered through a price range by inputting the lowest and highest price desired, then clicking `Submit Price`.
- **Search**: Users can search for items through both exact terms and relevant terms by typing in the search bar at the top of the page and then pressing the `Enter` key on their keyboard.

### Managing Inventory
> Note: Only available to validated Admin users
#### Adding Items
1. Navigate to Admin view
2. Click the blue `Add an Item` button located at the bottom left
3. Complete the required fields with:
    - Name
    - Size (dropdown menu)
    - Colour
    - Gender (dropdown menu)
    - Price
    - Stock (number in stock)
    - Brand
    - Image (upload an image)
4. Click `Save` to successfully upload item
5. Can either return by clicking `Back to Catalogue` or continue adding items

### Editing Items:
1. Locate item in Admin view
2. Click `Modify` on desired item
3. Modify desired fields
4. Click `Save` to successfully save changes

### Deleting Items:
1. Locate item in Admin view
2. Click `Modify` on desired item
3. Click `Delete Item` to successfully delete item
    > Note: If there are more than 10 items in the catalogue, the UI will prompt the user to confirm that they want to delete this item.

## Troubleshooting
### Common Issues:
- **Missing Data Files**:
    - System automatically creates required CSV files
        - Will create a `catalogue.csv` file if it does not already exist
    - Ensure write permissions in project directory
- **Image Upload Issues**:
    - Verify `static/images` directory exists
    - Check file permissions
    - Supported formats for addition through web application: PNG
    - Supported formats for manual CSV addition: PNG, JPG, JPEG, GIF
- **Authentication Problems**:
    - Verify `adminLogins.csv` exists
    - Check file format (CSV with `username,password` columns)
    - Ensure desired login information is correctly included in the CSV

## Testing
The system includes comprehensive unit tests that can be run using:
```bash
python build.py test
```

The unit tests cover:
- Clothing item creation
- User authentication
- Catalogue operations

## Future Enhancements
1. User Management:
    - Additional user roles
    - Password reset functionality
2. Advanced Features:
    - Inventory reporting
    - Barcode integration
3. UI Improvements:
    - Mobile-responsive design
    - Enhanced search interface