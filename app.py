from flask import Flask, render_template, request, redirect, url_for
from backEndShopLyft import ClothingItem, ClothingCatalogue # changed from "from ClothingItem import ClothingCatalogue" -Jordyn
# changed so it imports ClothingItem as well -Wingfung
import os # new

app = Flask(__name__)

catalogue = ClothingCatalogue()

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

info = []

def loadData():
    global info
    catalogue.load_items()
    info = []
    for item in catalogue.items:
        info.append(item.to_dict())

def loadBrands(): # retrives unique brands from catalogue
    brands = catalogue.get_filter_values('brand')
    # print(brands) # for debugging
    return brands.get('values', [])
        
def saveImages(image, itemName):
    try:
        image_filename = f"image_{itemName}.png"
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        image_path = image_path.replace('\\', '/')
        print(image_path)
        image.save(image_path)
    except Exception as e:
        print(f"Error: {e}")

@app.route('/')
def staff():
    loadData()
    return render_template('staff.html', cards = info, brands=loadBrands())

@app.route('/admin')
def admin():
    loadData()
    return render_template('admin.html', cards=info, brands=loadBrands())

@app.route('/add')
def add():
    return render_template('add.html', brands=loadBrands())

@app.route('/modify/<item_id>')
def modify(item_id):
    for item in info:
        if item['name'] == item_id:
            return render_template('modify.html', item=item, brands=loadBrands())
    else:
        return render_template('admin.html', cards=info, brands=loadBrands())

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
    saveImages(image, name)

    image_path = f'/images/image_{name}.png'
    new_item = ClothingItem(name, size, colour, gender, price, quantity, brand, image_path)
    catalogue.add_item(new_item)

    info.append(new_item.to_dict())

    return redirect(url_for('add'))

@app.route('/updateItem/<item_id>', methods=['POST'])
def updateItem(item_id):
    for item in info:
        if item['name'] == item_id:
            name = request.form.get('name')
            size = request.form.get('size')
            colour = request.form.get('colour')
            gender = request.form.get('gender')
            price = float(request.form.get('price'))
            quantity = int(request.form.get('stock'))  # 'stock' in the form corresponds to 'quantity' in the backend
            brand = request.form.get('brand')
            image = request.files['image']
            
            image_filename = f"image_{item['name']}.png"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image_path = image_path.replace('\\', '/')
            
            try:
                os.remove(image_path)
            except Exception as e:
                print(f'Error has occured {e}')
        
            saveImages(image, name)
            
            new_item = ClothingItem(name, size, colour, gender, price, quantity, brand, f'/images/image_{name}.png')
            catalogue.edit_item(item_id, new_item)
    
    return redirect(url_for('staff'))


if __name__ == '__main__':
    app.run(debug=True)