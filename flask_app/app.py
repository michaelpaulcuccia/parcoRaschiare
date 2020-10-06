from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('home.html')

#handle submit
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        park_choice = request.form['park_choice']
        print(park_choice)
        return render_template('success.html')

# run directly 
if __name__ == '__main__':
    app.debug = True
    app.run()
