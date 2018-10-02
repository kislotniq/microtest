from flask import Flask
import string

app = Flask(__name__)



def listCustomers():
    return [42, 93, 84, 13]

def getCustomerName(identifier):
    return 'John'



@app.route('/customers')
def presentationListCustomers():
    customer_ids = listCustomers()
    stringified_ids = [str(x) for x in customer_ids]
    return string.join(stringified_ids, '\n')


@app.route('/customers/<int:id>')
def presentationGetCustomer(id):
    # No need to sanitize id, looks like flask
    # properly handles non-integer values
    return getCustomerName(id) + '\n'
