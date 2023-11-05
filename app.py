from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', )

@app.route('/parking-grid')
def parking_grid():
    return render_template('parking-grid.html')

    elements = request.args.get('one', 'two', 'three', 'four', 'five', 'six')


if __name__ == '__main__':
    app.run(debug=True)