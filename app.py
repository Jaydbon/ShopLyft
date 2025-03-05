from flask import Flask, render_template, request, redirect, url_for
from backEndShopLyft import ClothingItem, ClothingCatalogue # changed from "from ClothingItem import ClothingCatalogue" -Jordyn
# changed so it imports ClothingItem as well -Wingfung
# from werkzeug.utils import secure_filename # new
# import os # new

app = Flask(__name__)

catalogue = ClothingCatalogue()
catalogue.load_items()
info = []
for item in catalogue.items:
    info.append(item.to_dict())

# # Configure upload folder and allowed extensions
# UPLOAD_FOLDER = 'static/images'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Ensure the upload folder exists
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# def allowed_file(filename):
#     """Check if the file has an allowed extension."""
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def get_next_image_number():
#     """Get the next available image number in the static/images folder."""
#     existing_files = os.listdir(app.config['UPLOAD_FOLDER'])
#     image_numbers = []
#     for file in existing_files:
#         if file.startswith("image ") and file.endswith(".png"):
#             try:
#                 number = int(file.split(" ")[1].split(".")[0])
#                 image_numbers.append(number)
#             except (IndexError, ValueError):
#                 continue
#     if image_numbers:
#         return max(image_numbers) + 1
#     return 1  # Start from 1 if no images exist

@app.route('/')
def staff():
    return render_template('staff.html', cards = info)

@app.route('/admin')
def admin():
    return render_template('admin.html', cards=info)

@app.route('/add')
def add():
    return render_template('add.html')


@app.route('/delete/<item_id>', methods=['POST'])
def deleteItem(item_id):
    global info
    for item in info:
        if item['name'] == item_id:
            catalogue.remove_item(item_id)

    # Remove the item from the info list
    info = [item for item in info if item['name'] != item_id]
    print(item_id)
    return redirect(url_for('admin'))

@app.route('/submit', methods=['POST'])
def submit():
    global info
    # Create a dictionary to store the form data
    name = request.form.get('name')
    size = request.form.get('size')
    colour = request.form.get('colour')
    gender = request.form.get('gender')
    price = float(request.form.get('price'))
    quantity = int(request.form.get('stock'))  # 'stock' in the form corresponds to 'quantity' in the backend
    brand = request.form.get('brand')
    image_path = ""

    # # Handle image upload
    # image_file = request.files.get('image')
    # image_path = ""
    # if image_file and allowed_file(image_file.filename):
    #     # Get the next available image number
    #     next_number = get_next_image_number()
    #     # Create the new filename
    #     filename = f"image {next_number}.png"
    #     # Save the file to the upload folder
    #     image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    #     image_file.save(image_path)
    #     # Store the relative path for use in the HTML template
    #     image_path = os.path.join('images', filename)

    # Create a ClothingItem object
    new_item = ClothingItem(name, size, colour, gender, price, quantity, brand, image_path)

    print(new_item)
    result = catalogue.add_item(new_item)

    # Update the info list
    info.append(new_item.to_dict())

    return redirect(url_for('add'))

if __name__ == '__main__':
    app.run(debug=True)