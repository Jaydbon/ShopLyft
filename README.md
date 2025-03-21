# ShopLyft Clothing Catalogue
## About the Project
This project provides an interactive clothing catalogue for managing stock. All users can search, sort, and filter items by keyword (TODO: and by related terms), as well as by attributes like brand, size, gender, and type. Admin users have additional permissions to add, remove, and edit stock items. Items are displayed with a short descriptive title, price, quantity in stock, and image.

## Built With:
- **Flask**: A lightweight web framework for building web applications.
- **Python**: The programming language used for both the backend logic and handling data.

## Prerequisites
- **Python 3.x** (Recommended version: 3.7 or higher)
    - Make sure python is installed on your system. You can download it from [python.org](https://www.python.org/downloads/)

## Dependencies
The following libraries and modules are used in the project:
- **Flask**: This is the web framework used to create the web application.
- **os**: Standard Python library used for interacting with the operating system (*e.g, handling file paths and directories*)
- **csv**: Standard Python library used to read from and write to CSV files that store clothing item data.
- **getpass**: Standard Python library used to securely prompt users for passwords.
- **subprocess**: Standard Python library used to execute shell commands from within Python. Used in this project to run commands like activating virtual environments, installing dependencies, starting the Flask application, and running tests.
- **sys**: Standard Python library used for interacting with the Python runtime environment. In this project it's used to handle command-line arguments and exit the script when necessary.

## Installing Dependencies
To install the required dependencies, follow these steps:
1. Install Flask
    - Run the following command to install Flask:
    ```bash
    pip install Flask
    ```

## Getting Started
1. **Clone the Repository**:
    - To clone the repository to your local machine, run:
    ```bash
    git clone https://github.com/Jaydbon/ShopLyft.git
    ```

2. **Run the Application**:
    - Navigate into the project directory:
    ```bash
    cd ShopLyft
    ```
    - Set up virtual environment:
    ```bash
    python -m venv venv
    ```
    - Activate virtual environment:
      
        - **For macOS/Linux:**
          ```bash
          source venv/bin/activate
          ```
        - **For Windows:**
          ```bash
          venv\Scripts\activate
          ```
    - Install required packages:
    ```bash
    pip install -r requirements.txt
    ```
    - Run the Flask application:
    ```bash
    python app.py
    ```
    - Open the provided URL in your web browser to access the website.
3. **Run the Application (Build Version)**:
    - Navigate into the project directory:
    ```bash
    cd ShopLyft
    ```
    - Set up virtual environment:
    ```bash
    python -m venv venv
    ```
    - Install required packages:
    ```bash
    python build.py install
    ```
    - Run the Flask application:
    ```bash
    python build.py run
    ```
    - Open the provided URL in your web browser to access the website (you may also run ```python build.py``` to check all commands).
## Features
### Staff Functions (Available to All Users)
1. **Staff Page**:
    - Access a list of all items currently in stock, with titles, prices, available quantities, and images.

### Admin Functions (Available to Admins Only)
1. **To Access the Admin Page**:
    - Click the **Admin** button located at the top right of the Staff Page to access Admin functionalities.
2. **To Add Items**:
    - Click the **Add Item** button located at the bottom left of the Admin Page.
    - Fill in the required fields to describe the item.
3. **To Delete Items**:
    - Click the **Delete** button next to any item to remove it from the catalogue.
4. **To Edit Items**: (To be implemented in Iteration II)
    - Admin users can edit item details (like price or quantity) from the Admin Page.
5. **To Access the Staff Page**:
    - From the Admin Page, click the **Staff** button on the top right to go back to the Staff Page.
> Note: Only Admin users have access to add, edit, or delete items.

## Troubleshooting
- **Missing CSV File**: The application will create a `catalogue.csv` file automatically if it does not already exist.
