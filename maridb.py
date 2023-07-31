import mariadb
from mariadb import IntegrityError
from dotenv import load_dotenv
import os
import sys
import logging


class DupEntry(Exception):
    pass

class maria_db(object):
    def __init__(self):
        logging.basicConfig(level=logging.ERROR,
                            format='%(asctime)s %(funcName)s %(msg)s',
                            filename='mariaDB-connector.log', filemode='a')
        load_dotenv()
        # Line above assumes that in the root directory (same level as your venv)
        # you have a .env file with permissions set to chmod 600, add .env to .gitignore,
        # which contains the following:
        # -------
        # DB_USER = "<...>"
        # DB_PASSWORD = "<...>"
        # DB_HOST = "<...>"
        # DB_SCHEMA = "<...>"
        # DB_PORT = "<...>"
        # -------
        # where <...> is *your* respective values to connect to the MariaDB

        db_config = {
            'user': os.environ.get('DB_USER'),
            'password': os.environ.get('DB_PASSWORD'),
            'host': os.environ.get('DB_HOST'),
            'port': int(os.environ.get('DB_PORT')),
            'database': os.environ.get('DB_SCHEMA')
        }
        try:
            self.db_connection = mariadb.connect(**db_config)
        except mariadb.Error as e:
            print("Error connecting to MariaDB: " + str({e}))
            logging.exception("Error connecting to MariaDB")
            sys.exit(1)
        except:
            e = sys.exc_info()[0]
            logging.exception("General error when connecting to MariaDB")
            print("General error when connecting to MariaDB: %s" % e)
            sys.exit(1)
        logging.exception("running with MariaDB on \'"+os.environ.get('DB_HOST')+"\'")
        print("running with MariaDB on \'"+os.environ.get('DB_HOST')+"\' db name = "+os.environ.get('DB_SCHEMA'))
        self.dicursor = self.db_connection.cursor(dictionary=True)
        self.noparams_cur = self.db_connection.cursor()
        self.trx_cur = self.db_connection.cursor()
        self.inscr_cur = self.db_connection.cursor()
        self.inscr_form_cur = self.db_connection.cursor()
        self.vin_cur = self.db_connection.cursor()
        self.vout_cur = self.db_connection.cursor()
        self.witcount_cur = self.db_connection.cursor()
        self.assert_cur = self.db_connection.cursor()
        self.trx_insert_cur = self.db_connection.cursor()
        self.vin_insert_cur = self.db_connection.cursor()
        self.vout_insert_cur = self.db_connection.cursor()
        self.lastinsert_cur = self.db_connection.cursor()
        self.witnessquery_cur = self.db_connection.cursor()

    def db_noparams_query(self, query):
        self.noparams_cur.execute(query)
        return self.noparams_cur

    def db_witness_query(self, query):
        self.witnessquery_cur.execute(query)
        return self.witnessquery_cur

    def db_inscr_query(self, query):
        self.inscr_cur.execute(query)
        return self.inscr_cur

    def db_inscr_format_query(self, query):
        self.inscr_form_cur.execute(query)
        return self.inscr_form_cur

    def db_trx_query(self, query):
        self.trx_cur.execute(query)
        return self.trx_cur

    def vin_query(self, query):
        self.vin_cur.execute(query)
        return self.vin_cur

    def vout_query(self, query):
        self.vout_cur.execute(query)
        return self.vout_cur

    def db_assert_query(self, query):
        # print(query)
        self.assert_cur.execute(query)

    def db_witcount_query(self, query):
        #  print(query)
        self.witcount_cur.execute(query)
        return self.witcount_cur

    def trx_insert(self, query):
        # print(query)
        try:
            self.trx_insert_cur.execute(query)
        except IntegrityError as e:
            if 'Duplicate entry' in str(e.args):
                raise DupEntry()

        return self.db_lastid()
    def vin_insert(self, query):
        try:
            self.vin_insert_cur.execute(query)
        except IntegrityError as e:
            if 'Duplicate entry' in str(e.args):
                raise DupEntry()
        return self.db_lastid()

    def vout_insert(self, query):
        try:
            self.vout_insert_cur.execute(query)
        except IntegrityError as e:
            if 'Duplicate entry' in str(e.args):
                raise DupEntry()
        return self.db_lastid()

    def db_lastid(self):
        query = 'SELECT LAST_INSERT_ID()'
       #  lastinsert_cur = self.db_connection.cursor()
        self.lastinsert_cur.execute(query)
        v_ret = self.lastinsert_cur.fetchone()
        # lastinsert_cur.close()
        return v_ret

    def db_noparams_fetchone(self, v_cur):
        return v_cur.fetchone()

    def db_inscr_fetchone(self, v_cur):
        return v_cur.fetchone()
    def fetchone_witness(self, v_cur):
        return v_cur.fetchone()

    def db_inscr_format_fetchone(self, v_cur):
        return v_cur.fetchone()

    def db_VinCur_Fetchone(self, v_kur):
        return v_kur.fetchone()
    def db_VoutCur_Fetchone(self, v_kuur):
        return v_kuur.fetchone()

    def db_cur_callproc(self, proc_name, params):
        self.dicursor.callproc(proc_name, params)

    def db_cur_execProc_return(self, proc_name, args):
        # args = [v_worker, v_running] <= for example
        self.discursor = self.db_connection.cursor()
        self.discursor.callproc(proc_name, args)
        v_ret = self.discursor.fetchone()
        self.discursor.close()
        return v_ret

    def db_commit(self):
        self.db_connection.commit()

    def db_rollback(self):
        self.db_connection.rollback()

    def __del__(self):
        self.db_connection.close()
