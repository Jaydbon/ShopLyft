from flask import Flask, render_template
from backend import ClothingCatalogue # changed from "from ClothingItem import ClothingCatalogue" -Jordyn

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


if __name__ == '__main__':
    app.run(debug=True)