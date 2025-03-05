from flask import Flask, render_template, request, redirect, url_for
from backEndShopLyft import ClothingItem, ClothingCatalogue # changed from "from ClothingItem import ClothingCatalogue" -Jordyn

app = Flask(__name__)

catalogue = ClothingCatalogue()
catalogue.load_items()
info = []
for item in catalogue.items:
    info.append(item.to_dict())


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
    image = request.form.get('image', "")

    # Create a ClothingItem object
    new_item = ClothingItem(name, size, colour, gender, price, quantity, brand, image)

    result = catalogue.add_item(new_item)

    return redirect(url_for('add'))

if __name__ == '__main__':
    app.run(debug=True)