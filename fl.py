from flask import Flask
from flask import request
import redis
from flask import abort

import string

app = Flask(__name__)
storage = redis.StrictRedis(host="redis", port=6379, db=0)



def isKeyword(key):
    return key in ['uid_counter']

def listCustomerIds():
    # TODO: what's the typical way of separating actual data
    #       from service data?
    ids = [key for key in storage.keys() if not isKeyword(key)]
    return ids

def getCustomerName(identifier):
    """
    Returns name or None if customer doesn't exist
    """
    return storage.get(identifier)

def setCustomerName(identifier, new_name):
    """
    Returns True if customer exists and name was set
    """
    if storage.get(identifier):
        return storage.set(identifier, new_name) and True

    return False

def createCustomer(name):
    """
    Returns customer id if customer was created,
    None otherwise
    """
    # TODO: how atomic is this incr?
    new_id = storage.incr('uid_counter')
    if not storage.setnx(new_id, name):
        return None
    return new_id


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
def presentationListCustomerIds():
    customer_ids = listCustomerIds()
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
