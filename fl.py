from flask import Flask
from flask import request
from flask import abort

import string

app = Flask(__name__)



def listCustomers():
    return [42, 93, 84, 13]

def getCustomerName(identifier):
    return 'John'

def setCustomerName(identifier, new_name):
    pass

def createCustomer(name):
    # TODO: atomically increment counter and get it's value
    #       create a new customer with the id
    pass


def nameIsAllowed(name):
    """
    Returns true if name consists of lower case
    latin letters
    """
    for character in name:
        if ord(character) < ord('a') or ord(character) > ord('z'):
            return False
    return True



@app.route('/customers')
def presentationListCustomers():
    customer_ids = listCustomers()
    stringified_ids = [str(x) for x in customer_ids]
    return string.join(stringified_ids, '\n')


@app.route('/customers/<int:cid>')
def presentationGetCustomer(cid):
    # No need to sanitize id, looks like flask
    # properly handles non-integer values
    customer_name = getCustomerName(cid)
    if customer_name:
        return customer_name
    else:
        abort(404, 'Error: customer "{cid}" not found'.format(cid=cid))


@app.route('/customers', methods=['PUT'])
def presentationCreateCustomer():
    name = request.args.get('name')

    if not name:
        abort(400, 'Error: "name" argument is mandatory')
    if not nameIsAllowed(name):
        abort(400, 'Error: only lower case lating letters allowed for "name"')

    customer_id = createCustomer(name)
    if customer_id:
        return 'Ok, id: {cid}'.format(cid=customer_id)
    else:
        abort(500, 'Error: failed to create customer')


@app.route('/customers/<int:id>', methods=['PUT'])
def presentationSetCustomerName(id):
    new_name = request.args.get("newName")

    if not new_name:
        abort(400, 'Error: "newName" argument is mandatory')
    if not nameIsAllowed(new_name):
        abort(400, 'Error: only lower case latin letters allowed for "newName"')

    if setCustomerName(id, new_name):
        return "Ok, new name: {n}\n".format(n=new_name)
    else:
        abort(500, 'Error: failed to set customer name')
