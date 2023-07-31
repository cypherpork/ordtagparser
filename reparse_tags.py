import logging
from queries import DBQueries as qq

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s %(funcName)s %(msg)s',
                    filename='ltrx.log', filemode='a')

Queries = qq()

def main():
    tags_cursor = Queries.ReparseTagsQuery()
    i = 0
    while True:
        i += 1
        row = Queries.fetchWitness(tags_cursor)
        if row is None:
            break
        Queries.updateTags(row)
        if i % 100 == 0:
            print('Processed: ' + str(i) +' rows')

    return i


if __name__ == "__main__":
    v_mesg = 'started'
    logging.error(v_mesg)
    num_rows = main()
    print('Processed', str(num_rows))
