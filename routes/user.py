from logging import DEBUG
import re
from server import *
from flask import Blueprint
from log.log import *
import asyncio
from mysql.sql_table import * 

print("========= start user.py =========")

# call Blueprint
bp = Blueprint("user", __name__, url_prefix='/')

# CRUD of information in mongoDB
'''
=======================================================================
GET   /                                           hello
GET   /info                                       find all
GET   /info/search?item=00&value=00               find item

POST   /info/insert                                insert info
POST   /info/update?usr_id=00&item=00&value=00       single update
POST   /info/state?usr_id=00&pid=00&value=00       update state
POST   /info/delete?id=00                           delete specific user
=======================================================================
'''

# search all information
@bp.route('/info', methods=['GET'])
async def user_search_all():
    info = mg_db.userinfo
    output = []

    for q in info.find():
        output.append({
            'usr': q['usr'],
            'prod_info': q['prod_info']
        })

    log.get_log('debug')

    return jsonify({'result': output})

# search by item
@bp.route('/info/search', methods=['GET'])
async def user_search():
    info = mg_db.userinfo
    item = request.args.get('item')
    value = request.args.get('value')

    usr = ['usr_id', 'age', 'email', 'phone', 'gender']
    prod_info = ['prod_id', 'category', 'state']

    output = []
    result = []

    if item in usr:
        if(item == 'age'):
            result = info.find({'usr.'+item: int(value)})
        else:
            result = info.find({'usr.'+item: value})

    elif item in prod_info:
        if item == 'state':
            result = info.find(
                {'prod_info.state.'+value: {"$regex": '2021.*'}})
        else:
            result = info.find({'prod_info.'+item: value})

    for q in result:
        output.append({
                        'usr': q['usr'],
                        'prod_info': q['prod_info']
            })
    log.get_log('debug')

    return jsonify({'result': output})


# async def test():
#     with app.test_request_context():
#         result = await user_search_all()
#         return result
        

# async def test2():
#     with app.test_request_context():
#         result = await user_search()
#         return result

async def total():
    with app.test_request_context():
        task1 = user_search_all()
        task2 = user_search()

        result1 = await task1
        result2 = await task2

        if( user_search_all == True):
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaa")
            return result1
        elif( user_search == True):
            print("bbbbbbbbbbbbbbbbbbbbbbbbb")
            return result2

# loop = asyncio.get_event_loop()
# loop.run_until_complete(test())
# loop.close()
print("test()")
asyncio.run(total(), debug = True)

print("test2")
# asyncio.run(test2())

# # add information
@bp.route('/info/insert', methods=['POST'])
def user_insert_thread():
    print("this is insert_info()")
    dict_q = {'url' : request.url, 'data' : request.json}
    queue.put(dict_q)
    log.get_log('debug')
    return ('end insert_info')

def user_insert(data):
    info = mg_db.userinfo
    
    usr = data['usr']
    prod_info = data['prod_info']
    prod_id = info.insert({'usr': usr, 'prod_info':prod_info})
    new_prod = info.find_one({'_id': prod_id})

    output = {
        'usr': new_prod["usr"],
                    'prod_info': new_prod['prod_info']
        }

    return output

# update specific item
@bp.route('/info/update', methods=["POST"])
def user_update_thread():
    print("this is update_info()")
    dict_q = {'url' : request.url, 'data' : dict(request.values)}
    queue.put(dict_q)
    log.get_log('debug')

    return ('end update_info')

def user_update(data):
    info = mg_db.userinfo

    id = data.get('id')
    value = data.get('value')
    item = data.get('item')

    q = info.find_one({'usr.usr_id': id})

    usr = ['usr_id', 'age', 'email', 'phone', 'gender']

    if item in usr:
        if(item == 'age'):
            value = int(value)
        newvalues = {
            "$set": {
                'usr.'+item: value
                }}

    update = info.update_one({'usr.usr_id': id}, newvalues)
    output = []

    if q:
        update
        output = 'Update success'

    else:
        output = 'cannot update info'

    return output

# update state
@bp.route('/info/state', methods=["POST"])
def user_state_thread():
    print("update_info_state")

    dict_q = {'url' : request.url, 'data' : dict(request.values)}

    queue.put(dict_q)

    log.get_log('debug')
    return ('end update_info_state')


def user_state(data):
    id = data.get('id')
    pid = data.get('pid')
    value = data.get('value')

    info = mg_db.userinfo

    q = info.find_one(
        {"$and": [{'usr.usr_id': id}, {'prod_info.p_id': pid}]})

    prod_info = q['prod_info']

    for i in prod_info:
        if i['p_id'] == pid:
            state = i['state']

    state[value] = datetime.now().isoformat()

    newvalues = {
        "$set": {
            'prod_info.$.state': state
        }
    }

    update = info.update(
        {"$and": [{'usr.usr_id': id}, {'prod_info.p_id': pid}]}, newvalues)

    if q:
        update
        output = 'Update success'
    else:
        output = 'cannot update info'

    return output

# delete information
@bp.route("/info/delete", methods=['POST'])
def user_delete_thread():
    print('put_q_delete')
    dict_q = {'url' : request.url, 'data' : dict(request.values)}
    queue.put(dict_q)
    log.get_log('debug')

    return('end put_q_delete')

def user_delete(data):
    info = mg_db.userinfo

    id = data.get('id')

    q = info.find_one({'usr.usr_id': id})
    delete = info.delete_one({'usr.usr_id': id})

    output = []

    if q:
        delete
        output = 'Delete Success'

    else:
        output = 'You cannot delete info'

    return output

# ==================================================================
# CRUD of usr in mysql db

# getUsrList[GET] :  http://10.10.10.182:5151/usr
# getOne    [GET] :  http://10.10.10.182:5151/usr/select?usr_id=user05
# insert    [POST] : http://10.10.10.182:5151/usr/insert?usr_id=user06&email=user06@gamail.com&gender=W&phone=010-1234-5555&age=22
# update    [POST] : http://10.10.10.182:5151/usr/update?usr_id=user06&email=user66@gamil.com&gender=M&phone=010-1234-1234&age=33
# delete    [POST] : http://10.10.10.182:5151/usr/delete?usr_id=user06

# search all usr
@bp.route('/usr', methods=['GET'])
def usr_search_all():

    usr_list = UsrDAO().get_usr()
    log.get_log('debug')

    return jsonify(usr_list)

# search usr one
@bp.route('/usr/select', methods=['GET'])
def usr_get_one():
    usr_id = request.args.get('usr_id')

    if(usr_id == None):
        log.get_log('info')
        return 'please enter the USR_ID...'
    else:
        usr_one = UsrDAO().get_one_usr(usr_id)
        if(usr_one == None):
            log.get_log('info')
            return 'please check the USR_ID...'
        else:
            log.get_log('debug')
            return jsonify({'select SUCCESS' : usr_one})

# insert usr information
@bp.route('/usr/insert', methods=['POST'])
def usr_insert():
    usr_id = request.args.get('usr_id')
    email = request.args.get('email')
    gender = request.args.get('gender')
    phone = request.args.get('phone')
    age = request.args.get('age')

    if(usr_id == None):
        log.get_log('info')
        return 'please enter the USR_ID...'
    elif(email == None):
        log.get_log('info')
        return 'please enter the EMAIL...'
    else:
        if(UsrDAO().get_one_usr(usr_id) != None):
            log.get_log('info')
            return 'ID is already exist...'
        elif(UsrDAO().email_check(email) != None):
            log.get_log('info')
            return 'EMAIL is already exist...'
        else:
            UsrDAO().insert_usr(usr_id, email, gender, phone, age)
            log.get_log('debug')
            return jsonify({'insert SUCCESS':UsrDAO().get_one_usr(usr_id)})

# update usr information
@bp.route('/usr/update', methods=['POST'])
def usr_update():
    usr_id = request.args.get('usr_id')
    email = request.args.get('email')
    gender = request.args.get('gender')
    phone = request.args.get('phone')
    age = request.args.get('age')

    if(usr_id == None):
        log.get_log('info')
        return 'please enter the USR_ID...'
    else:
        if(UsrDAO().get_one_usr(usr_id) == None):
            log.get_log('info')
            return 'please check the USR_ID...'
        elif(email != None):
            check_email = UsrDAO().email_check(email)
            if((check_email != None) and (check_email.get('usr_id') != usr_id)):
                log.get_log('info')
                return 'EMAIL is already exist...'
            else:
                log.get_log('debug')
                UsrDAO().update_usr(usr_id, email, gender, phone, age)
                return jsonify({'update SUCCESS': UsrDAO().get_one_usr(usr_id)})                    
        else:
            log.get_log('debug')
            UsrDAO().update_usr(usr_id, email, gender, phone, age)
            return jsonify({'update SUCCESS': UsrDAO().get_one_usr(usr_id)})

# delete usr information
@bp.route('/usr/delete', methods=['POST'])
def usr_delete():
    usr_id = request.args.get('usr_id')

    if(usr_id == None):
        log.get_log('info')
        return 'please check the USR_ID...'
    else :
        usr_one = UsrDAO().get_one_usr(usr_id)
        if(usr_one == None):
            log.get_log('info')
            return 'please check the USR_ID...'
        else: 
            log.get_log('debug')
            UsrDAO().delete_usr(usr_id)
            return ('delete SUCCESS')

# ======================================================================
# CRUD of usr_product in mysql db

# getUsrList[GET] :  http://10.10.10.182:5151/product
# getOne    [GET] :  http://10.10.10.182:5151/product/select?prod_id=tableA
# insert    [POST] : http://10.10.10.182:5151/product/insert?prod_id=tableB&usr_id=user02&state_id=1&cate_id=4&price=79800
# update    [POST] : http://10.10.10.182:5151/product/state?prod_id=tableB&usr_id=user02&state_id=2
# delete    [POST] : http://10.10.10.182:5151/product/delete?prod_id=tableB&usr_id=user02&state_id=2

# search all usr_product
@bp.route('/product', methods=['GET'])
def usr_product_search_all():

    prod_list = ProductDAO().get_product_all()
    log.get_log('debug')

    return jsonify(prod_list)

# search usr_product one
@bp.route('/product/select', methods=['GET'])
def usr_prod_get():
    prod_id = request.args.get('prod_id')

    if(prod_id == None):
        log.get_log('info')
        return 'please enter the PROD_ID...'
    else:
        prod_one = ProductDAO().get_product(prod_id)
        if(prod_one == None):
            log.get_log('info')
            return 'please check the PROD_ID...'
        else:
            log.get_log('debug')
            return jsonify({'select SUCCESS' : prod_one})

# insert usr_product information
@bp.route('/product/insert', methods=['POST'])
def usr_prod_insert():
    prod_id = request.args.get('prod_id')
    usr_id = request.args.get('usr_id')
    state_id = request.args.get('state_id')
    cate_id = request.args.get('cate_id')
    price = request.args.get('price')

    if(usr_id == None):
        log.get_log('info')
        return 'please enter the USR_ID...'
    elif(prod_id == None):
        log.get_log('info')
        return 'please enter the PROD_ID...'
    else:
        if(ProductDAO().get_one_product(prod_id) != None):
            log.get_log('info')
            return 'PROD_ID is already exist...'
        else:
            log.get_log('debug')
            ProductDAO().insert_product(prod_id, usr_id, state_id, cate_id, price)
            return jsonify({'insert SUCCESS':ProductDAO().get_one_product(prod_id)})

# delete usr_product information
@bp.route('/product/delete', methods=['POST'])
def usr_prod_delete():
    prod_id = request.args.get('prod_id')
    usr_id = request.args.get('usr_id')
    state_id = request.args.get('state_id')
    
    if(prod_id == None or usr_id == None or state_id == None):
        log.get_log('info')
        return 'check items...'
    else:
        log.get_log('debug')
        ProductDAO().delete_product(prod_id, usr_id, state_id)

    return 'delete SUCCESS'

# update usr_product state information to mysql db
@bp.route('/product/state', methods=['POST'])
def usr_update_state():
    usr_id = request.args.get('usr_id')
    prod_id = request.args.get('prod_id')
    state_id = request.args.get('state_id')

    data = ProductDAO().get_usr_product(prod_id, usr_id)

    if len(data) == 0:
        log.get_log('info')
        return 'data is not exist'

    else:
        for d in data:
            ProductDAO().update_state(prod_id, usr_id, int(state_id), d['cate_id'], d['price'])
        log.get_log('debug')

    return jsonify({'update SUCCESS': ProductDAO().get_usr_product(prod_id, usr_id)})    

@bp.route('/product/getavg', methods=['GET'])
def usr_get_avg():
    prod_id = request.args.get('prod_id')
    state_id = request.args.get('state_id')

    return ProductDAO().get_avg(prod_id, state_id)


