from server import *
 
curs = mysql_db.cursor()
 
class UsrDAO:
 
    def __init__(self):
        pass
 
    def get_usr(self):
        ret = []
 
        query = "select * from usr"
        curs.execute(query)
 
        rows = curs.fetchall()
        for e in rows:
            temp = {'usr_id': e[0], 'email': e[1],
                    'gender': e[2], 'phone': e[3], 'age': e[4]}
            ret.append(temp)
 
        return ret
 
    def get_one_usr(self, usr_id):
        ret = []
        query = "select * from usr where usr_id=%s"
        curs.execute(query, (usr_id))
        ret = curs.fetchone()
        while ret:
            return {'usr_id': ret[0], 'email': ret[1], 'gender': ret[2], 'phone': ret[3], 'age': ret[4]}
 
 
    def insert_usr(self, usr_id, email, gender, phone, age):
        query = '''insert into usr (usr_id, email, gender, phone, age) values(%s, %s, %s, %s, %s)'''
        curs.execute(query, (usr_id, email, gender, phone, age))
        mysql_db.commit()
 
    def email_check(self, email):
        print('email check')
        ret = []
        query = "select * from usr where email=%s"
        curs.execute(query, (email))
        ret = curs.fetchone()
        while ret:
            return {'usr_id': ret[0], 'email': ret[1], 'gender': ret[2], 'phone': ret[3], 'age': ret[4]}
 
    def update_usr(self, usr_id, email, gender, phone, age):
        query = "update usr set "
        q_col = []
        exe_col = []
 
        if (email != None):
            q_col.append('email=%s')
            exe_col.append(email)
        if (gender != None):
            q_col.append('gender=%s')
            exe_col.append(gender)
        if (phone != None):
            q_col.append('phone=%s')
            exe_col.append(phone)
        if (age != None):
            q_col.append('age=%s')
            exe_col.append(age)
 
        q_col = ', '.join(q_col)
        query += q_col
 
        query += " where usr_id=%s"
        exe_col.append(usr_id)
        exe = tuple(exe_col)
 
        curs.execute(query, exe)
        mysql_db.commit()
 
    def delete_usr(self, usr_id):
        query = "delete from usr where usr_id=%s"
        curs.execute(query, usr_id)
        mysql_db.commit()
 
 
class ProductDAO:
 
    def __init__(self):
        pass
 
    # get usr information in mysql db
    def get_product_all(self):
        ret = []
 
        query = "select * from usr_product"
        curs.execute(query)
 
        # all of data
        rows = curs.fetchall()
        for e in rows:
            temp = {'prod_id': e[0], 'usr_id': e[1],
                    'state_id': e[2], 'cate_id': e[3], 'time': e[4], 'price': e[5]}
            ret.append(temp)
 
        return ret
 
    # get one usr information in mysql db
    def get_one_product(self, prod_id):
        ret = []
        query = "select * from usr_product where prod_id=%s"
        curs.execute(query, (prod_id))
 
        # one of data
        ret = curs.fetchone()
 
        while ret:
            return {'prod_id': ret[0], 'usr_id': ret[1],
                    'state_id': ret[2], 'cate_id': ret[3], 'time': ret[4], 'price': ret[5]}
 
    def get_product(self, prod_id):
        ret = []
        query = "select * from usr_product where prod_id=%s"
        curs.execute(query, (prod_id))
 
        # all of data
        rows = curs.fetchall()
        for e in rows:
            temp = {'prod_id': e[0], 'usr_id': e[1],
                    'state_id': e[2], 'cate_id': e[3], 'time': e[4], 'price': e[5]}
            ret.append(temp)
 
        return ret
 
    # insert usr_product information to mysql db
    def insert_product(self, prod_id, usr_id, state_id, cate_id, price):
        now = datetime.now()
        time = now.strftime('%Y-%m-%d %H:%M:%S')
 
        query = '''insert into usr_product (prod_id, usr_id, state_id, cate_id, time, price) values(%s, %s, %s, %s, %s, %s)'''
        curs.execute(query, (prod_id, usr_id, state_id, cate_id, time, price))
        mysql_db.commit()
 
    # delete usr_product information in mysql db
    def delete_product(self, prod_id, usr_id, state_id):
        query = "delete from usr_product where prod_id=%s and usr_id=%s and state_id=%s"
        curs.execute(query, (prod_id, usr_id, state_id))
        mysql_db.commit() 
 
    # get product information in mysql db
    def get_usr_product(self, prod_id, usr_id):
        ret = []
        query = "select * from usr_product where prod_id=%s and usr_id=%s"
        curs.execute(query, (prod_id, usr_id))
        rows = curs.fetchall()
 
        for e in rows:
            temp = {'prod_id': e[0], 'usr_id': e[1],
                    'state_id': e[2], 'cate_id': e[3], 'time': e[4], 'price': e[5]}
            ret.append(temp)
 
        return ret
 
    # update product information to mysql db
    def update_state(self, prod_id, usr_id, state_id, cate_id, price):
        now = datetime.now()
        time = now.strftime('%Y-%m-%d %H:%M:%S')
        
        #query = "insert ignore into usr_product (prod_id, usr_id, state_id, cate_id, time, price) values(%s, %s, %s, %s, %s, %s)"
        query = "replace into usr_product (prod_id, usr_id, state_id, cate_id, time, price) values(%s, %s, %s, %s, %s, %s)"
        curs.execute(query, (prod_id, usr_id, state_id, cate_id, time, price))
        mysql_db.commit()

    def get_avg(self, prod_id, state_id):
        query = """select avg(u.age) 
                    from usr_product p
                    left join usr u on p.usr_id = u.usr_id
                    where prod_id like %s and state_id in (%s);"""
        curs.execute(query, (prod_id, state_id))

        return f"{prod_id} 항목, {state_id} 상태인 유저의 평균 나이 : {curs.fetchone()[0]}"


