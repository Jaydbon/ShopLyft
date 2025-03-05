from flask import Flask, render_template
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


# @app.route('/delete/<item_id>', methods=['POST'])
# def deleteItem(item_id):
#     if item_id in info:
#         del info[item_id]
#     return render_template('admin.html', cards=info)

if __name__ == '__main__':
    app.run(debug=True)