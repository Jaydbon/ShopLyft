from flask import Flask, render_template, request, redirect, url_for
from backEndShopLyft import ClothingCatalogue # changed from "from ClothingItem import ClothingCatalogue" -Jordyn

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


@app.route('/delete/<item_id>', methods=['POST'])
def deleteItem(item_id):
    global info
    item_to_delete = None
    for item in catalogue.items:
        if item.name == item_id:
            catalogue.remove_item(item)

    # Remove the item from the info list
    info = [item for item in info if item['name'] != item_id]
    print(item_id)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)