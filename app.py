from flask import Flask, render_template, request, redirect, url_for
from backEndShopLyft import ClothingItem, ClothingCatalogue # changed from "from ClothingItem import ClothingCatalogue" -Jordyn
# changed so it imports ClothingItem as well -Wingfung
import os # new
import csv

app = Flask(__name__)

catalogue = ClothingCatalogue()

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

info = []
sortBy = 'name'
activeFilters = {"brand":[], "price":[]}
searchStr = ""
previousPage =""

def loadUsers():
    users = []
    with open('adminLogins.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users.append(row)
    return users

@app.route('/login', methods=['POST', 'GET'])
def login(): 
    return render_template('login.html')

@app.route('/logged', methods=['POST', 'GET'])
def logged():
    username = request.form.get('username')
    password = request.form.get('password')
    users = loadUsers()
    for log in users:
        if username == log['username'] and password == log['password']:
            return redirect(url_for('admin'))
    return redirect(url_for('login'))


@app.route('/priceUpdate', methods=["POST"])
def priceUpdate():
    low = request.form.getlist('low')
    high = request.form.getlist('high')
    print(low)
    print(high)
    activeFilters["price"] = [low[0],high[0]]

    print(activeFilters)
    return redirect(url_for(previousPage))

@app.route('/search', methods=["POST"])
def search():
    global searchStr
    searchStr = request.form['search']
    print(searchStr)
    return redirect(url_for(previousPage))

def setSearch():
    if searchStr != "" and searchStr != "search":
        inf = catalogue.search_items(searchStr)['matching_items']
        if inf == []:
            return catalogue.find_related_items(searchStr)['related_items']
        return inf 
    else:
        return info

@app.route('/filters', methods=['GET', 'POST'])
def add_Filters():
    global activeFilters
    activeFilters["brand"] = request.form.getlist('brand') if request.method == 'POST' else []
    activeFilters["size"] = request.form.getlist('size') if request.method == 'POST' else []
    activeFilters["gender"] = request.form.getlist('gender') if request.method == 'POST' else []
    activeFilters["colour"] = request.form.getlist('colour') if request.method == 'POST' else []
    return redirect(url_for(previousPage))

def set_Filters():
    return catalogue.get_filtered_items(activeFilters)['filtered_items']
    
def loadInfo():
    global info
    sortItems()
    catalogue.load_items()
    info = [item.to_dict() for item in catalogue.items]
    return info

def loadFilterOptions(option):
    options = catalogue.get_filter_values(option).get('values', [])
    return options


@app.route('/sorter', methods=['POST'])
def sorter():
    global sortBy
    sortBy = request.form['dropdown_value']
    catalogue.sort_items(sortBy)
    return redirect(url_for(previousPage))

def sortItems():
    catalogue.sort_items(sortBy)
        
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
    global info, previousPage
    info = loadInfo()
    info = set_Filters()
    info = setSearch()
    previousPage = 'staff'
    return render_template('staff.html', cards=info, brands=loadFilterOptions('brand'), types=loadFilterOptions('colour'), sortBy=sortBy, activeFilters=activeFilters)

@app.route('/admin')
def admin():
    global info, previousPage
    info = loadInfo()
    info = set_Filters()
    info = setSearch()
    previousPage = 'admin'
    print(f'load search: {info}')
    return render_template('admin.html', cards=info, brands=loadFilterOptions('brand'), types=loadFilterOptions('colour'), sortBy=sortBy, activeFilters=activeFilters)

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
            if item['quantity'] >= 10:
                return f"""
                <p>The stock count is higher than 10 are you sure you want to delete?</p>
                <form action="/confirm-delete/{item_id}" method="post">
                    <button type="submit">Confirm</button>
                </form>
                """
            catalogue.remove_item(item_id)

    info = [item for item in info if item['name'] != item_id]
    return redirect(url_for('admin'))

@app.route('/confirm-delete/<item_id>', methods=['POST'])
def confirmDeleteItem(item_id):
    global info
    for item in info:
        if item['name'] == item_id:
            catalogue.remove_item(item_id)
            return redirect(url_for(previousPage))

    return render_template('modify.html', item=item)


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
            if image != "":
                saveImages(image, name)
            # image_filename = f"image_{item['name']}.png"
            # image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            # image_path = image_path.replace('\\', '/')
            
            # try:
            #     os.remove(image_path)
            # except Exception as e:
            #     print(f'Error has occured {e}')
        
            saveImages(image, name)
            
            new_item = ClothingItem(name, size, colour, gender, price, quantity, brand, f'/images/image_{name}.png')
            catalogue.edit_item(item_id, new_item)
    
    return redirect(url_for('staff'))


if __name__ == '__main__':
    app.run(debug=True)