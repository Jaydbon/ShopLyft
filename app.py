from flask import Flask, render_template, request, redirect, url_for
from backEndShopLyft import ClothingItem, ClothingCatalogue # changed from "from ClothingItem import ClothingCatalogue" -Jordyn
# changed so it imports ClothingItem as well -Wingfung
import os # new

app = Flask(__name__)

catalogue = ClothingCatalogue()
catalogue.load_items()
info = []
for item in catalogue.items:
    info.append(item.to_dict())

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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

    info = [item for item in info if item['name'] != item_id]
    print(item_id)
    return redirect(url_for('admin'))

@app.route('/submit', methods=['POST'])
def submit():
    global info

    name = request.form.get('name')
    size = request.form.get('size')
    colour = request.form.get('colour')
    gender = request.form.get('gender')
    price = float(request.form.get('price'))
    quantity = int(request.form.get('stock'))  # 'stock' in the form corresponds to 'quantity' in the backend
    brand = request.form.get('brand')
    image = request.files['image']
    if image and allowed_file(image.filename):
        image_number = len(info)+1
        print(image_number)
        image_filename = f"image_{image_number}.png"
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        image_path = image_path.replace('\\', '/')
        image.save(image_path)
    else:
        image_path = ""

    image_path = image_path[6::]
    new_item = ClothingItem(name, size, colour, gender, price, quantity, brand, image_path)
    catalogue.add_item(new_item)

    info.append(new_item.to_dict())

    return redirect(url_for('add'))

if __name__ == '__main__':
    app.run(debug=True)