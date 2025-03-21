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
sortBy = 'name'
activeFilters = {"brand":[]}


@app.route('/filters', methods=['GET', 'POST'])
def add_Filters():
    global activeFilters
    activeFilters["brand"] = request.form.getlist('brand') if request.method == 'POST' else []
    activeFilters["size"] = request.form.getlist('size') if request.method == 'POST' else []
    activeFilters["gender"] = request.form.getlist('gender') if request.method == 'POST' else []
    activeFilters["colour"] = request.form.getlist('colour') if request.method == 'POST' else []
    print(activeFilters)
    return redirect(url_for('staff'))

def set_Filters():
    newInfo = catalogue.get_filtered_items(activeFilters)['filtered_items']
    return newInfo
    
def loadInfo():
    global info
    catalogue.load_items()
    info = [item.to_dict() for item in catalogue.items]
    return info

def loadFilterOptions(option):
    options = catalogue.get_filter_values(option).get('values', [])
    return options


@app.route('/sorter', methods=['POST'])
def sortItems():
    global sortBy
    sortBy = request.form['dropdown_value']
    catalogue.sort_items(sortBy)
    return redirect(url_for('staff'))

        
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
    info = loadInfo()
    info = set_Filters()
    return render_template('staff.html', cards=info, brands=loadFilterOptions('brand'), types=loadFilterOptions('colour'), sortBy=sortBy, activeFilters=activeFilters)

@app.route('/admin')
def admin():
    info = loadInfo()
    return render_template('admin.html', cards=info, brands=loadFilterOptions('brand'), types=loadFilterOptions('colour'), sortBy=sortBy)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/modify/<item_id>')
def modify(item_id):
    for item in info:
        if item['name'] == item_id:
            return render_template('modify.html', item=item)
    else:
        return render_template('admin.html', cards=info)

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