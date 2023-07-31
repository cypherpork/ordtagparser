import hashlib
from maridb import maria_db as Marusja
from maridb import DupEntry
from dotenv import load_dotenv
import logging
import os
from massage import MassageData as MassageData
import btcpy.structs.script as script
import binascii

DataTLC = MassageData()


class DBQueries(object):
    def __init__(self):
        load_dotenv()
        logging.basicConfig(level=logging.ERROR,
                            format='%(asctime)s %(funcName)s %(msg)s',
                            filename='lqueries.log', filemode='a')
        self.mari = Marusja()
        try:
            self.rpcnet = os.environ.get('BTC_CHAIN')
        except:
            logging.exception("Trouble getting BTC_CHAIN from .env")
            raise EnvironmentError

    def CursedQuery(self):  # todo: change here
        try:
            selectquery = "select inscr.* from inscr, non_01_tags where inscr.chain = '" \
                          + self.rpcnet \
                          + "' and inscr.`status` = \'PROC\'" \
                          + " and inscr.id = non_01_tags.id" \
                          + " and (non_01_tags.parstatus = \'NEW\' or non_01_tags.parstatus = \'ERR\') order by id"
                          #  + " and ord_id < 0 and id < 57522 " \
            print(selectquery)
            return self.mari.db_noparams_query(selectquery)  # cursor
        except:
            logging.exception("CursedQuery0 is in trouble")
            raise RuntimeError

    def ComprehensiveQuery(self):  # todo: change here
        try:
            selectquery = "select * from inscr where chain = '" \
                          + self.rpcnet \
                          + "' and `status` = \'PROC\'" \
                          + " and (parstatus = \'NEW\' or parstatus = \'ERR\') order by id"
                          #  + " and ord_id < 0 and id < 57522 " \
            print(selectquery)
            return self.mari.db_noparams_query(selectquery)  # cursor
        except:
            logging.exception("CursedQuery0 is in trouble")
            raise RuntimeError

    def ReparseTagsQuery(self):
        try:
            selectquery = "select * from ord_tags where chain = '" \
                          + self.rpcnet \
                          + "' and tag_no <> \"01\" order by id"
                          #  + " and ord_id < 0 and id < 57522 " \
            print(selectquery)
            return self.mari.db_noparams_query(selectquery)  # cursor
        except:
            logging.exception("CursedQuery0 is in trouble")
            raise RuntimeError
    def witnessQuery(self):
        try:
            selectquery = "select * from wit where" \
                          + " rstatus = \'NEW\'" \
                          + " order by id asc"
            # print(selectquery)
            # selectquery = "select * from wit where " \
            #               + " rstatus = \'NEW\'" \
            #               + " and content_format = \'TBD\' " \
            #               + " order by id asc"
            # print(selectquery)
            return self.mari.db_witness_query(selectquery)
        except:
            logging.exception("witnessQuery is in trouble")
            raise RuntimeError

    def fetchWitness(self,in_cursor):
        return self.mari.fetchone_witness(in_cursor)


    def updateWitness(self, in_wrow):
        pkid = in_wrow[0]
        withex_val = in_wrow[6]
        # print(withex_val)
        witbytes = bytes.fromhex(withex_val)
        withash = hashlib.md5(witbytes).hexdigest()
        unwrapped=self.unwrapWitness(withex_val)
        bwit = bytes.fromhex(withex_val)
        # bunhexed = bytes.fromhex(withex_val).decode("utf-8").replace("\"", "\\\"")
        # unhexed = DataTLC.sanitize(bunhexed)
        unhexed = binascii.hexlify(bwit).decode()
        v_update = "update wit set unwrapped_content = \"" + str(unwrapped) + \
                   "\", unhexlified_cont = \"" + unhexed + \
                   "\", rstatus = \"" + "PROC" + "\", hashwit = \"" + \
                   str(withash) + "\" where id = " + str(pkid)
        # print(v_update)
        try:
            self.mari.db_assert_query(v_update)
            self.mari.db_commit()
        except:
            self.mari.db_rollback()
            logging.exception("Trouble updating witness for id=" + str(pkid))
            raise RuntimeError

    def updateTags(self, in_trow):
        pkid = in_trow[0]
        tag_no = in_trow[3]
        tag_value = in_trow[4]
        # print(tag_value)
        new_guess, new_note, notation_id = DataTLC.guessTag(tag_no, tag_value)
        if tag_no != '01':
            v_update = "update ord_tags set tag_guess = \"" + new_guess + \
                       "\", `note` = \"" + new_note + \
                       "\", `notation_id` = " + str(notation_id) + \
                       " where id = " + str(pkid)
        else:
            v_update = "update ord_tags set tag_guess = \"" + new_guess + \
                       "\", `note` = \"" + new_note + \
                       "\", `format_notation` = " + str(notation_id) + \
                       " where id = " + str(pkid)
        # print(v_update)
        try:
            self.mari.db_assert_query(v_update)
            self.mari.db_commit()
        except:
            self.mari.db_rollback()
            logging.exception("Trouble updating transaction tags for id=" + str(pkid))
            raise RuntimeError

    def PrepInscrData(self, in_tb_id):
        try:
            selectquery = "select * from inscr where chain = \"" \
                          + self.rpcnet \
                          + "\" and id = " + str(in_tb_id)
            return self.mari.db_noparams_query(selectquery)  # cursor
        except:
            logging.exception("getInscrData is in trouble")
            raise RuntimeError

    def GetInscrFormat(self, in_tb_id):
        try:
            selectquery = "select tag_guess from ord_tags where chain = \"" \
                          + self.rpcnet \
                          + "\" and inscr_tb_id = " + str(in_tb_id) \
                          + " and tag_no = \"01\""
            v_cur = self.mari.db_inscr_format_query(selectquery)  # cursor
            v_format = self.mari.db_inscr_format_fetchone(v_cur)
            if v_format is None:
                return "n/a"
            else:
                return v_format[0]
        except:
            logging.exception("GetInscrFormat is in trouble")
            raise RuntimeError

    def FindInscrFormat(self, in_gen_tx, in_input):
        try:
            selectquery = "select ord_tags.tag_guess from ord_tags, inscr where inscr.chain = \"" \
                          + self.rpcnet \
                          + "\" and inscr.id = ord_tags.inscr_tb_id" \
                          + " and inscr.gen_trx = \"" + in_gen_tx \
                          + "\" and inscr.output_no = " + str(in_input) \
                          + " and ord_tags.tag_no = \"01\" LIMIT 1"
            # print(selectquery)
            v_cur = self.mari.db_inscr_format_query(selectquery)  # cursor
            v_format = self.mari.db_inscr_format_fetchone(v_cur)
            if v_format is None:
                return "n/a"
            else:
                return v_format[0]
        except:
            logging.exception("GetInscrFormat is in trouble")
            raise RuntimeError

    def getInscrRow(self, querycursor):
        try:
            return self.mari.db_inscr_fetchone(querycursor)  # row
        except:
            logging.exception("getInscrRow is in trouble")
            raise RuntimeError

    def StartQuery(self):
        try:
            selectquery = "select * from inscr where chain = '" \
                          + self.rpcnet + \
                          "' and `status` <> \'PROC\'"
                          # " and id between <partitionStart> and <partitionEnda>"
            logging.exception("chain =" + self.rpcnet)
            return self.mari.db_noparams_query(selectquery)  # cursor
        except:
            logging.exception("startQuery is in trouble")
            raise RuntimeError
    def getTxRow(self, querycursor):
        try:
            return self.mari.db_noparams_fetchone(querycursor)  # row
        except:
            logging.exception("getTxRow is in trouble")
            raise RuntimeError

    def insertTags(self, in_id, in_ordid, in_tagno, in_tagvalue):
        try:
            v_int_tagno = int(in_tagno)
        except:
            v_int_tagno = int(in_tagno, base=16)
            in_tagno = str(v_int_tagno)
        v_tag_guess, v_tag_note = DataTLC.guessTag(in_tagno, in_tagvalue)
        v_insert = "insert into ord_tags (inscr_tb_id, ord_id, tag_no, tag_value, tag_guess, `chain`, note) values ("+ \
                   str(in_id) + ", " + str(in_ordid) + ", \"" + str(in_tagno) + "\", \"" + \
                   str(in_tagvalue) + "\", \"" + v_tag_guess +"\",\""+self.rpcnet+"\", \""+v_tag_note+"\")"
        # print(v_insert)
        self.mari.db_assert_query(v_insert)

    def updateFirst(self):
        v_update = "UPDATE inscr SET gen_trx = " \
                   "LEFT ( inscr_id, 64 ), " \
                   "output_no = RIGHT(inscr_id,(LENGTH( inscr_id )- 65 )) " \
                   "where chain = \'"+ self.rpcnet + "\'"
        try:
            self.mari.db_assert_query(v_update)
            self.mari.db_commit()
        except:
            self.mari.db_rollback()
            logging.exception("First Update is in trouble")
            raise RuntimeError

    def updateTagno(self, in_id, in_adj_outp_no, in_num_tags, in_ok, in_is_tag1_present):
        if in_ok:
            if in_is_tag1_present:
                v_status = 'PROC'
            else:
                v_status = 'NOTAG1'
        else:
            v_status = 'ERR'
        if in_adj_outp_no == None:
            in_adj_outp_no = -1
        v_update = "update inscr set num_tags = " + str(in_num_tags) + \
                   ", `status` = \'" + v_status + "\', adj_output_no = " + \
                   str(in_adj_outp_no) + " where id = " + str(in_id)
        # print(v_update)
        try:
            self.mari.db_assert_query(v_update)
            self.mari.db_commit()
        except:
            self.mari.db_rollback()
            logging.exception("Trouble during tagparsing while updating status for id=" + str(in_id))
            raise RuntimeError

    def shadowUpdateInscrStatus(self, in_id, in_trxid, in_inputs, in_outputs, in_ok, in_shadowing=0):
        if in_ok == 0:
            v_message = 'parsed ' + str(in_inputs) + ' inputs and ' \
                        + str(in_outputs) + ' outputs; trxid = ' + str(in_id)
            if in_shadowing == 0:
                v_status = 'PROC'
            else:
                v_status = 'PHANTOM'
        else:
            v_status = 'ERR'
            v_message = 'Error'

        v_update = "update inscr set trxid = " + str(in_trxid) + \
                   ", parstatus = \'" + v_status + "\', parmessage = \'" + \
                   v_message + "\', shadowing = "+str(in_shadowing)+" where id = " + str(in_id)
        # print(v_update)
        try:
            self.mari.db_assert_query(v_update)
            self.mari.db_commit()
            return in_id
        except:
            self.mari.db_rollback()
            logging.exception("Trouble during shadowparsing while updating status for id=" + str(in_id))
            raise

    def getIDforTx(self, in_txid):
        v_cur = self.mari.db_trx_query("select id from tx where txid = \""+str(in_txid)+"\"")
        return self.mari.db_noparams_fetchone(v_cur)

    def getIDforVin(self, in_intxid, in_voutn):
        v_cur = self.mari.vin_query("select id from vin where intxid = \"" + str(in_intxid) +"\" and invoutn = "+str(in_voutn))
        return self.mari.db_VinCur_Fetchone(v_cur)

    def getIDforVout(self, in_belongsto_fkid, in_n):
        v_cur = self.mari.vout_query("select id from vout where belongsto_fkid = \"" + str(in_belongsto_fkid) + "\" and n = "+str(in_n))
        return self.mari.db_VoutCur_Fetchone(v_cur)

    def getWitSize(self, in_verbosetx, in_vin_no):
        try:
            witsize = len(in_verbosetx['vin'][in_vin_no]['txinwitness'])
        except IndexError:
            witsize = 0
        # print(witsize)
        return witsize

    def getRecordedWit(self, in_vin_no):
        v_query = "select count(1) from wit where fkid_vin_tab = " + str(in_vin_no)
        return self.mari.db_witcount_query(v_query)

    def wipeRecordedWit(self, in_vin_no):
        v_query = "delete from wit where fkid_vin_tab = " + str(in_vin_no)
        self.mari.db_assert_query(v_query)


    def insertTx(self, in_verbosetx):
        # print(in_verbosetx)
        v_insert = "insert into tx " \
                   + "(txid, hash, " \
                   + "version, txsize, txvsize, " \
                   + "weight, locktime, " \
                   + "vincount, voutcount, " \
                   + "blockhash, unixtime, " \
                   + "txtimedate, chainnet) values ( "\
                   + "\"" + in_verbosetx['txid'] + "\", \"" + in_verbosetx['hash'] + "\", " \
                   + str(in_verbosetx['version']) + ", " + str(in_verbosetx['size']) + ", " + str(in_verbosetx['vsize']) \
                   + ", " + str(in_verbosetx['weight']) + ", "+ str(in_verbosetx['locktime']) \
                   + ", " + str(len(in_verbosetx['vin'])) + ", " + str(len(in_verbosetx['vout'])) \
                   + ", \"" + str(in_verbosetx['blockhash']) + "\", " + str(in_verbosetx['time']) \
                   + ", " + "from_unixtime(" + str(in_verbosetx['time']) + ", '%Y-%m-%d %h:%i:%s'), \"" + self.rpcnet \
                   + "\")"
        # print(v_insert)
        try:
            try:
                out_id = (self.mari.trx_insert(v_insert))[0]
           #      self.mari.db_commit()
            except DupEntry:
                out_id = self.getIDforTx(in_verbosetx['txid'])[0]
        except:
           #  self.mari.db_rollback()
            logging.exception("Inserting TxID =" + in_verbosetx['txid'])
            raise
        return out_id

    def insertVins(self, in_verbosetx, tx_pk_id, in_contentformat, in_content_inputno, in_adj_content_inputno):
        if in_adj_content_inputno == -1:
            in_adj_content_inputno = in_content_inputno
        out_num_TxInputs = len(in_verbosetx['vin'])
        # print(out_num_TxInputs)
        content_format = "n/a"
        for input_no in range(out_num_TxInputs):
            #  print("I_no:",input_no)
            witsize = self.getWitSize(in_verbosetx, input_no)
          #  content_format = in_contentformat
            if input_no == in_content_inputno:
                if in_content_inputno == in_adj_content_inputno:
                    content_status = 'EXPECTED'
                    content_format = in_contentformat
                else:
                    content_status = 'FANTOM'
                    content_format = 'TBD'
            elif input_no == in_adj_content_inputno:
                    content_status = 'ASSUMED'
                    content_format = in_contentformat
            else:
                content_status = 'NONE'
                content_format = "n/a"

            vin_id = self.insertVin(in_verbosetx, tx_pk_id, input_no, witsize, content_status)

            #  print("vin_id",vin_id,"witsize",witsize )
            self.insertWits(in_verbosetx, vin_id, tx_pk_id, input_no, witsize, content_format)
        self.mari.db_commit()
        return out_num_TxInputs

    def insertVin(self, in_verbosetx, in_tx_pk_id, in_vin_no, in_witsize, in_content_status):
        v_insertvin = "insert into vin " \
                   + "(belongsto_fkid, idxvin, intxid, invoutn, vinseq, witsize, content_status) values ( " \
                   + str(in_tx_pk_id)+ ", "+ str(in_vin_no) + ", \"" + in_verbosetx['vin'][in_vin_no]['txid'] + "\", " \
                   + str(in_verbosetx['vin'][in_vin_no]['vout']) + ", " \
                   + str(in_verbosetx['vin'][in_vin_no]['sequence']) + ", " \
                   + str(in_witsize) + ", \"" + in_content_status + "\")"
        # print(v_insertvin)
        try:
            vin_id = (self.mari.vin_insert(v_insertvin))
            real_vin_id = vin_id[0]
        except DupEntry:
            arrayish_real_vin_id = self.getIDforVin(in_verbosetx['vin'][in_vin_no]['txid'], str(in_verbosetx['vin'][in_vin_no]['vout']))
            real_vin_id = arrayish_real_vin_id[0]
        return real_vin_id

    def insertWits(self, in_verbosetx, in_vin_id, in_tx_pk_id, in_vin_no, in_witsize, in_contentformat):
        if in_witsize != 0:
            v_recorded_wit = self.getRecordedWit(in_vin_id)
            if in_witsize != v_recorded_wit:
                if v_recorded_wit != 0:
                    self.wipeRecordedWit(in_vin_id)
            for v_idxwit in range(in_witsize):
                if v_idxwit == in_witsize -2:
                    if in_contentformat:
                        contentformat = in_contentformat
                    else:
                        contentformat = 'None Supplied'
                else:
                    contentformat = "n/a"
                self.insertWit(in_verbosetx, in_vin_id, in_tx_pk_id, in_vin_no, v_idxwit, contentformat)
        else:
            pass

    def insertWit(self, in_verbosetx, in_vin_id, in_tx_pk_id, in_idxvin, in_idxwit, in_contentformat):
        v_insert = "insert into wit " \
                   + "(fkid_vin_tab, belongsto_fkid_txid, idxvin, idxwit, " \
                   + "withex, content_format) values ( "\
                   + str(in_vin_id) + ", " + str(in_tx_pk_id) + ", " + str(in_idxvin)+ ", " + str(in_idxwit) + ", \"" \
                   + str(in_verbosetx['vin'][in_idxvin]['txinwitness'][in_idxwit]) + "\", \""+in_contentformat+"\")"
        # print(v_insert)
        try:
            wiut_id = self.mari.trx_insert(v_insert)
            self.mari.db_commit()
            return wiut_id
        except:
             logging.exception("Inserting witness TxID =" + in_verbosetx['txid'])
             raise

        ###############################
    def insertVouts(self, in_verbosetx, tx_pk_id):
        out_num_TxOutputs = len(in_verbosetx['vout'])
        #  print(out_num_TxOutputs)
        for output_no in range(out_num_TxOutputs):
            # print("Output no:", output_no)
            vout_id = self.insertVout(in_verbosetx, tx_pk_id, output_no)
            addrqty = self.howManyAddresses(in_verbosetx, output_no)
            # print("vout_id",vout_id,"pubksize",addrqty )
            self.insertAddresses(in_verbosetx, output_no, vout_id, addrqty)
        self.mari.db_commit()
        return out_num_TxOutputs

    def insertVout(self, in_verbosetx, out_id, in_out_no):
        v_insertvout = "insert into vout " \
                       + "(belongsto_fkid, valu, n, pkasm, pkdesc, pkhex, pktype, reqsigs) values ( " \
                       + str(out_id) + ", " + str(in_verbosetx['vout'][in_out_no]['value']) + ", " \
                       + str(in_verbosetx['vout'][in_out_no]['n']) + ", \"" \
                       + str(in_verbosetx['vout'][in_out_no]['scriptPubKey']['asm']) + "\", \"" \
                       + str(in_verbosetx['vout'][in_out_no]['scriptPubKey']['desc']) + "\", \"" \
                       + str(in_verbosetx['vout'][in_out_no]['scriptPubKey']['hex']) + "\", \"" \
                       + str(in_verbosetx['vout'][in_out_no]['scriptPubKey']['type']) + "\", " \
                       + str(self.howmanyReqSigs(in_verbosetx, in_out_no)) + ")"
        # print(v_insertvout)
        try:
            vout_id = (self.mari.vout_insert(v_insertvout))
            real_vout_id = vout_id[0]
        except DupEntry:
            real_vout_id = self.getIDforVout(out_id, in_verbosetx['vout'][in_out_no]['n'])[0]
        return real_vout_id

    def howManyAddresses(self, in_verbosetx, in_vout_no):
        try:
            addrqty = len(in_verbosetx['vout'][in_vout_no]['scriptPubKey']['addresses'])
        except KeyError:
            try:
                v_address = in_verbosetx['vout'][in_vout_no]['scriptPubKey']['address']
                return 1
            except KeyError:
                return 0

    def howmanyReqSigs(self, in_verbosetx, in_vout_no):
        try:
            return int(in_verbosetx['vout'][in_vout_no]['scriptPubKey']['reqSigs'])
        except KeyError:
            try:
                v_address = in_verbosetx['vout'][in_vout_no]['scriptPubKey']['address']
                return 1
            except KeyError:
                return 0

    def insertAddresses(self, in_verbosetx, in_vout_no, in_real_vout_id, in_addrqty):
        if in_addrqty == 1:
            addr_idx = 0
            out_addr = in_verbosetx['vout'][in_vout_no]['scriptPubKey']['address']
            self.insertAddress(out_addr, in_real_vout_id, addr_idx)
        else:
            for addr_idx in range(in_addrqty):
                out_addr = in_verbosetx['vout'][in_vout_no]['scriptPubKey']['addresses'][addr_idx]
                self.insertAddress(out_addr, in_real_vout_id, addr_idx)
        return addr_idx

    def insertAddress(self, addr_to_insert, in_real_vout_id, in_addr_idx):
        v_insert = "insert into addr " \
                   + "(fkid, addridx, " \
                   + "pkaddr) values ( "\
                   + str(in_real_vout_id) + ", " + str(in_addr_idx) + ", \"" \
                   + addr_to_insert + "\")"
        # print(v_insert)
        try:
            addr_id = self.mari.trx_insert(v_insert)
            return addr_id
        except:
             logging.exception("Inserting Address query =" + v_insert)
             raise RuntimeError

    def unwrapWitness(self, in_hex):
        return str(script.Script.unhexlify(in_hex))