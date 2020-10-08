from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import bs4, requests

#define app
app = Flask(__name__)

#environment
ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    #database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:182201xx!@localhost/nps_scrape'
else:
    app.debug = False 

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Database Object
db = SQLAlchemy(app)

#model
class ParkContactData(db.Model):
    __tablename__ = 'parkcontactdata'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True)
    streetaddress = db.Column(db.String(200))
    state = db.Column(db.String(200))
    zipCode = db.Column(db.String(200))
    phone = db.Column(db.String(200))

    def __init__(self, title, streetaddress, state, zipCode, phone):
        self.title = title
        self.streetaddress = streetaddress
        self.state = state
        self.zipCode = zipCode
        self.phone = phone

@app.route('/')
def home_page():
    return render_template('home.html')

#handle submit
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':

        #unique 4 letter park key for URL - source home.html, <select name="park_choice"></select>
        park_choice = request.form['park_choice']
        
        #build URL Request
        pre_url = 'https://www.nps.gov/'
        park_var = park_choice
        suf_url = '/index.htm'
        url = pre_url + park_var + suf_url

        #make URL request, get response code/status, entire page returns as 'soup'
        res = requests.get(url)
        print('Res Status Code: ' + str(res.status_code)) #200
        print('Any Issues: ' + str(res.raise_for_status())) #none
        soup = bs4.BeautifulSoup(res.text, 'html.parser')

        #title
        title = soup.find('a', class_ = 'Hero-title')
        title_text = title.get_text()

        #street address
        street_address = soup.find('span', class_ = 'street-address')
        street_address_text = street_address.get_text()
                
        #state
        state_abrv = soup.find('span', class_ = 'region')
        state_text = state_abrv.get_text()      

        #zip
        zip_code = soup.find('span', class_ = 'postal-code')
        zip_code_text = zip_code.get_text()      

        #phone
        phone = soup.find('span', class_ = 'tel')
        phone_text = phone.get_text()     

        #dictionary containing all data
        park_address = {
            'title': title_text,
            'address': street_address_text,
            'state': state_text,
            'zipCode': zip_code_text,
            'phone': phone_text
        }
        
        #message for success page containing all fields
        response_string = park_address['title'] + ' Address: ' + park_address['address'] + ', ' + park_address['state'] + ', ' + park_address['zipCode'] + ' phone: ' + park_address['phone']

        #post to Postgresql
        '''
        payload = ParkContactData(title_text, street_address_text, state_text, zip_code_text, phone_text)
        db.session.add(payload)
        db.session.commit()
        '''
        
        #success page and message
        return render_template('success.html', response_data=response_string)   
        
    else:
        
        error_string = 'sorry, there was a request error. request.method !== POST'

        return render_template('success.html', response_data=error_string)

# run directly 
if __name__ == '__main__':
    app.run()
 