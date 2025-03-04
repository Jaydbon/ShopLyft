from flask import Flask, render_template
from backend import ClothingCatalogue # changed from "from ClothingItem import ClothingCatalogue" -Jordyn

app = Flask(__name__)

@app.route('/')
def staff():
    catalogue = ClothingCatalogue()
    catalogue.load_items()
    return render_template('staff.html', cards = catalogue.items)

@app.route('/admin')
def admin():
    catalogue = ClothingCatalogue()
    catalogue.load_items()
    return render_template('admin.html', cards=catalogue.items)


if __name__ == '__main__':
    app.run(debug=True)