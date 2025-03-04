from flask import Flask, render_template
from ClothingItem import ClothingCatalogue
app = Flask(__name__)

@app.route('/')
def staff():
    catalogue = ClothingCatalogue()
    catalogue.load_items()
    return render_template('staff.html', cards = cards)










if __name__ == '__main__':
    app.run(debug=True)