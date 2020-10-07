from flask import Flask, render_template, request
import bs4, requests
app = Flask(__name__)

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

        #ParkFooter-contact
        '''
        park_footer = soup.find('div', class_ = 'ParkFooter-contact')
        print('Scrape: ' + str(park_footer))
        '''

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

        park_address = {
            'address': street_address_text,
            'state': state_text,
            'zipCode': zip_code_text,
            'phone': phone_text
        }
        
        response_string = park_address['address'] + ', ' + park_address['state'] + ', ' + park_address['zipCode'] + ' phone: ' + park_address['phone'] 

        return render_template('success.html', response_data=response_string)

    else:
        
        error_string = 'sorry, there was a request error. request.method !== POST'

        return render_template('success.html', response_data=error_string)

# run directly 
if __name__ == '__main__':
    app.debug = True
    app.run()
