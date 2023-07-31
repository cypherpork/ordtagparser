import asyncio
import logging
from queries import DBQueries as qq
from noda import BTCnoda as Noda
from massage import MassageData as MassageData
import sys


logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s %(funcName)s %(msg)s',
                    filename='lparser.log', filemode='a')

FromNoda = Noda()
Queries = qq()
DataTLC = MassageData()

def insertArray(in_id, in_ordid, in_tagarr):
    for i in range(0, len(in_tagarr)):
        if len(in_tagarr[i][0]) > 2:
            logging.error("Invalid Tag ID, Trx ID: " + str(in_ordid) + "; data: " + str(in_tagarr))
            raise RuntimeError
        elif in_tagarr[i][1] is None:
            logging.error("Invalid Tag value, Trx ID: " + str(in_ordid) + "; data: " + str(in_tagarr))
            raise RuntimeError
        else:
            Queries.insertTags(in_id, in_ordid, in_tagarr[i][0], in_tagarr[i][1])


async def process_row(in_row):
    try:  # we iterate here because misplaced output is frequent in the source tsv
        adjusted_outp_no = in_row[4]
        v_is_tag1_present = False
        v_is_tag1_present, adjusted_outp_no, tags = await FromNoda.getTxTags(in_row[3], in_row[4])
        tagarr = DataTLC.shapeTagArray(tags)
        insertArray(in_row[0], in_row[1], tagarr)
        v_num_tags = len(tagarr)
        v_ok = True
    except:
        v_num_tags = -1
        v_ok = False
        logging.error("Error parsing Row ID = " + str(in_row[0]))
        raise  # todo: this
    Queries.updateTagno(in_row[0], adjusted_outp_no, v_num_tags, v_ok, v_is_tag1_present)
    if v_ok:
        return 0
    else:
        return 1


async def main():
    q = 0
    v_errcount = 0
    Queries.updateFirst()
    query_cursor = Queries.StartQuery()

    while True:
        row = Queries.getTxRow(query_cursor)
        if row is None:
            break
        v_this_result = await process_row(row)
        v_errcount = v_errcount + v_this_result
        q += 1
        if q % 1000 == 0:
            print(' ', end="\r", flush=True)
            print('Processed: ' + str(q) + ' rows and ' + str(v_errcount) + ' errors so far...')
        row = []
    v_mesg = 'finished, processed ' + str(q) + ' rows and ' + str(v_errcount) + ' errors.'
    print(v_mesg)
    logging.error(v_mesg)
    sys.exit(0)


if __name__ == "__main__":
    v_mesg = 'started'
    logging.error(v_mesg)
    print(v_mesg)
    asyncio.run(main())
