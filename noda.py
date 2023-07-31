from dotenv import load_dotenv
import os
from bitcoinrpc import BitcoinRPC
import btcpy.structs.script as script
import re
import logging
import sys
from massage import MassageData as MassageData
import time

DataTLC = MassageData()

class BTCnoda(object):
    def __init__(self):
        load_dotenv()
        try:
            self.rpc_hostline = os.environ.get('BTC_RPC_PROTOCOL') + \
                                '://' + os.environ.get('BTC_RPC_HOST') + \
                                ':' + os.environ.get('BTC_RPC_PORT')
            self.rpc_un = os.environ.get('BTC_RPC_USER')
            self.rpc_pw = os.environ.get('BTC_RPC_PASSWORD')
        except:
            logging.exception("Getting connect data for Bitcoin node")
            sys.exit(1)
        logging.basicConfig(level=logging.ERROR,
                            format='%(asctime)s %(funcName)s %(msg)s',
                            filename='lnoda.log', filemode='a')
        try:
            self.rpcnet = os.environ.get('BTC_CHAIN')
        except:
            logging.exception("Trouble getting BTC_CHAIN from .env")
            raise EnvironmentError
        logging.exception("running with Bitcoin " + self.rpcnet + " node at \'" + self.rpc_hostline + "\'")
        print("running with Bitcoin " + self.rpcnet + " node at \'" + self.rpc_hostline + "\'")

    async def getTx(self, in_trxid):
        i = 0
        while i < 11:
            i += 1
            try:
                async with BitcoinRPC.from_config(self.rpc_hostline, (self.rpc_un, self.rpc_pw)) as rpc:
                        verbosetx = (await rpc.getrawtransaction(in_trxid, True))
                return verbosetx
            except:
                time.sleep(1)
        if i == 11:
            logging.exception("Crap, query from Bitcoin node failed, connect OK ID = " + str(in_trxid))
            sys.exit(1)


    def searchForTags(self, in_verbosetx, in_starting_input, in_verbose):
        if in_verbose:
            print(in_verbosetx)
        if in_starting_input > 0:  # if input is positive it could be lesser because of an ord bug:
            v_end = -1
            v_step = -1
        else:  # if input is 0 it could be more because of an ord bug:
            v_end = 99  # todo: this number is arbitrary. Need to pull it from json
            v_step = 1
        # iterate because tsv sometimes has wrong input nums (THE ord bug):
        for adjusted_input_no in range(in_starting_input, v_end,
                                       v_step):
            if in_verbose:
                print('ain=', adjusted_input_no)
            try:
                txwitness_size = len(in_verbosetx['vin'][adjusted_input_no]['txinwitness'])
                if in_verbose:
                    print('txwitnes size: ', txwitness_size)
            except IndexError:
                if in_verbose:
                    print('IndexError on witness size')
                if adjusted_input_no == v_end - v_step:
                    return False, -1, '00 INVALID_ENVELOPE'
                else:
                    continue
            # we assume that the witness stack that we want is the second from the end
            num_witness = txwitness_size - 2
            if num_witness < 0:
                continue
            try:
                hex_witness = in_verbosetx['vin'][adjusted_input_no]['txinwitness'][num_witness]
                if in_verbose:
                    print('hex_witness: ', hex_witness)
            except IndexError:
                if in_verbose:
                    print('IndexError on hex witness')
                continue
            unwrapped_witness = str(script.Script.unhexlify(hex_witness))
            if in_verbose:
                print('unwrapped_witness=', unwrapped_witness)
            # looking for text between 'OP_0 OP_IF 6f7264 ' and the second occurrence of 'OP_0':
            result = re.search('OP_0 OP_IF 6f7264 ' + '(.*?){2}' + 'OP_0', unwrapped_witness)
            if in_verbose:
                print('result=', result)
            if result is None:
                if adjusted_input_no == v_end-v_step:
                    return False, -1, '00 INVALID_ENVELOPE'
                else:
                    continue
            else:
                return True, adjusted_input_no, result.group(1)

    async def getTxTags(self, in_trxid, in_input_no=0, in_verbose=False):
        try:
            verbosetx = await self.getTx(in_trxid)
            search_success, adjusted_input_no, search_result = self.searchForTags(verbosetx, in_input_no, in_verbose)
            if in_verbose:
                print('search_success=', search_success, 'adjusted_input_no=', adjusted_input_no, 'search_result=', search_result)

            if search_success:
                is_tag1_present, return_words = DataTLC.purifyTags(search_result.split())
                return is_tag1_present, adjusted_input_no, return_words
            else:
                return False, adjusted_input_no, search_result.split()
        except:
            logging.exception("Getting trx tags from Bitcoin node for trxid =" + in_trxid)
            raise



