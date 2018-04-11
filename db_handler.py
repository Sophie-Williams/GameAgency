from configparser import ConfigParser
from mysql.connector import MySQLConnection, Error

from datetime import datetime
import time


class db_handler:


    def read_db_config(self, filename='config.ini', section='mysql'):
        """ Read database configuration file and return a dictionary object
        :param filename: name of the configuration file
        :param section: section of database configuration
        :return: a dictionary of database parameters
        """
        # create parser and read ini configuration file
        parser = ConfigParser()
        parser.read(filename)

        # get section, default to mysql
        db = {}
        if parser.has_section(section):
            items = parser.items(section)
            for item in items:
                db[item[0]] = item[1]
        else:
            raise Exception('{0} not found in the {1} file'.format(section, filename))

        return db

# ____________________________________________________________________________________________
# Блок получения выборок из базы

    def query_with_fetchone(self):
        try:
            dbconfig = self.read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM department")

            row = cursor.fetchone()

            while row is not None:
                print(row)
                row = cursor.fetchone()

        except Error as e:
            print(e)

        finally:
            cursor.close()
            conn.close()

    def search_admin(self):
        # query_with_fetchall возвращает список id администраторов
        try:
            result = []
            dbconfig = self.read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM admins")
            rows = cursor.fetchall()
            for row in rows:
                result.append(row[0])
            return result

        except Error as e:
            print(e)

        finally:
            cursor.close()
            conn.close()

    def iter_row(self, cursor, size=10):
        while True:
            rows = cursor.fetchmany(size)
            if not rows:
                break
            for row in rows:
                yield row

    def query_with_fetchmany(self):
        try:
            dbconfig = self.read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM admins")
            for row in self.iter_row(cursor, 10):
                print(row)
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()


    def query_with_fetchall(self, args):
        try:
            result = []
            query = "SELECT * FROM list_of_games WHERE owner=%s"
            #args =
            dbconfig = self.read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute(query, args)
            rows = cursor.fetchall()
            for row in rows:
                result.append(row)
            return result

        except Error as e:
            print(e)

        finally:
            cursor.close()
            conn.close()

    def query_with_fetchall2(self, args):
        try:
            result = []
            query = "SELECT * FROM list_of_games WHERE id=%s"
            #args =
            dbconfig = self.read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute(query, args)
            rows = cursor.fetchall()
            for row in rows:
                result.append(row)
            return result

        except Error as e:
            print(e)

        finally:
            cursor.close()
            conn.close()

    def select_levels(self, args):
        try:
            result = []
            query = "SELECT * FROM levels WHERE game_id=%s"
            #args =
            dbconfig = self.read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute(query, args)
            rows = cursor.fetchall()
            for row in rows:
                result.append(row)
            return result

        except Error as e:
            print(e)

        finally:
            cursor.close()
            conn.close()

    def select_level(self, args):
        try:
            result = []
            query = "SELECT * FROM levels WHERE id=%s"
            #args =
            dbconfig = self.read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute(query, args)
            rows = cursor.fetchall()
            for row in rows:
                result.append(row)
            return result[0]

        except Error as e:
            print(e)

        finally:
            cursor.close()
            conn.close()
#____________________________________________________________________________________________
# Блок записи в базу

    def insert_admins(self, id_admin, name_admin):
        query = "INSERT INTO admins(id,name) VALUES(%s,%s)"
        args = (id_admin, name_admin)
        try:
            db_config = self.read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            cursor.execute(query, args)
            #if cursor.lastrowid:
            #    print('last insert id', cursor.lastrowid)
            #else:
            #    print('last insert id not found')
            conn.commit()
        except Error as error:
            print(error)
        finally:
            cursor.close()
            conn.close()

    def insert_games(self, game):
        query = "INSERT INTO list_of_games(id,name,description, number_of_levels,date,owner) VALUES(%s,%s,%s,%s,%s,%s)"
        #game = tuple(game)
        arg = []
        tup = tuple(item for item in game)
        arg.append(tup)
        #print(arg)
        try:
            db_config = self.read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            cursor.executemany(query, arg)
            conn.commit()
        except Error as e:
            print('Error:', e)
        finally:
            cursor.close()
            conn.close()

    def create_levels(self, game_id, lev):
        query = "INSERT INTO levels(id,game_id,sn) VALUES(%s,%s,%s)"
        for i in range(lev):
            try:
                id = str(int(time.time())+i)[3:]
                db_config = self.read_db_config()
                conn = MySQLConnection(**db_config)
                cursor = conn.cursor()
                cursor.executemany(query, [(id, game_id, i+1)])
                conn.commit()
            except Error as e:
                print('Error:', e)
            finally:
                cursor.close()
                conn.close()

# ____________________________________________________________________________________________
# Блок внесения изменений в базу

    def update_game(self, param, value, id):
        if param == 'date':
            query = "UPDATE list_of_games SET date=%s WHERE id=%s"
        elif param == 'name':
            query = "UPDATE list_of_games SET name=%s WHERE id=%s"
        elif param == 'dscr':
            query = "UPDATE list_of_games SET description=%s WHERE id=%s"

        if param == 'header':
            query = "UPDATE levels SET header=%s WHERE id=%s"
        elif param == 'task':
            query = "UPDATE levels SET task=%s WHERE id=%s"
        elif param == 'answer':
            query = "UPDATE levels SET answer=%s WHERE id=%s"
        elif param == 'tip':
            query = "UPDATE levels SET tip=%s WHERE id=%s"

        arg = (value, id)
        try:
            db_config = self.read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            cursor.execute(query, arg)
            conn.commit()
        except Error as e:
            print('Error:', e)
        finally:
            cursor.close()
            conn.close()


# ____________________________________________________________________________________________
# Удаление строк

    def delete_book(self, game_id):
        query = "DELETE FROM list_of_games WHERE id = %s"
        try:
            # connect to the database server
            db_config = self.read_db_config()
            conn = MySQLConnection(**db_config)
            # execute the query
            cursor = conn.cursor()
            cursor.execute(query, (game_id,))
            # accept the change
            conn.commit()
        except Error as error:
            print(error)
        finally:
            cursor.close()
            conn.close()

    def delete_all_levels(self, game_id):
        query = "DELETE FROM levels WHERE game_id = %s"
        try:
            # connect to the database server
            db_config = self.read_db_config()
            conn = MySQLConnection(**db_config)
            # execute the query
            cursor = conn.cursor()
            cursor.execute(query, (game_id,))
            # accept the change
            conn.commit()
        except Error as error:
            print(error)
        finally:
            cursor.close()
            conn.close()


if __name__ == '__main__':

    #print(db_handler().query_with_fetchall([235987482]))
    #print(db_handler().query_with_fetchall2([1522305332]))
    #db_handler().update_name(name='UPDATE',id_game=1522305332)
    #db_handler().create_levels(555, 5)
    x = db_handler().select_level([3345586])
    print(x)
