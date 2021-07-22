'''
Created on Jan 10, 2017

@author: hanif
'''

import pymysql


class Database:
    def connect(self):
        # return pymysql.connect("fr-mysql", "dev", "dev", "crud_flask")

        return pymysql.connect(host="fr-mysql", user="dev", password="dev", database="crud_flask", charset='utf8mb4')

    def getuser(self, token):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            sql = "SELECT * FROM `token_table` WHERE `token`=%s"
            cursor.execute(sql, (token,))
            result = cursor.fetchone()
            return result
        except:
            return []
        finally:
            con.close()

    def logapicall(self, user_id):
        try:
            con = Database.connect(self)
            cursor = con.cursor()
            cursor.execute("INSERT INTO api_log(user_id) VALUES(%s)",
                           (user_id,))
            con.commit()
            return True
        except:
            return ()
        finally:
            con.close()

    def read(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM token_table order by id asc")
            else:
                cursor.execute(
                    "SELECT * FROM token_table order by id asc", (id,))

            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def insert(self, data):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("INSERT INTO phone_book(name,phone,address) VALUES(%s, %s, %s)",
                           (data['name'], data['phone'], data['address'],))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def update(self, id, data):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("UPDATE phone_book set name = %s, phone = %s, address = %s where id = %s",
                           (data['name'], data['phone'], data['address'], id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def delete(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("DELETE FROM phone_book where id = %s", (id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()
