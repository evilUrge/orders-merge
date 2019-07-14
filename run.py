import argparse
import logging
from os import environ

from base import Merger
from utils import BASE_DIR, DEBUG, DOCKER

if __name__ == '__main__':
    logging.basicConfig(filename='merge.log', format='%(levelname)s: %(message)s',
                        level=logging.DEBUG if DEBUG else logging.INFO)

    if DEBUG:
        Merger(barcodes_source=BASE_DIR + '/example/barcodes.csv',
               orders_source=BASE_DIR + '/example/orders.csv').execute(top=5,
                                                                       output_filename='demo',
                                                                       json=True)

    elif DOCKER:
        Merger(barcodes_source=environ.get('barcodes_source'),
               orders_source=environ.get('orders_source')).execute(top=environ.get('top'),
                                                                   output_filename=environ.get('filename'),
                                                                   json=environ.get('json'))

    else:
        parser = argparse.ArgumentParser(description='Orders merge - transform 2 datasets to one')
        parser.add_argument('-b', '--barcodes', metavar='Barcodes source',
                            help='Path for the barcodes_source csv file', required=True)
        parser.add_argument('-o', '--orders', metavar='Orders Source',
                            help='Path for the orders source csv file', required=True)
        parser.add_argument('-t', '--top', metavar='Top customers',
                            help="Integer of the top customers", required=False)
        parser.add_argument('-f', '--filename', metavar='Filename of the output',
                            help="Give a name for the output file (default result", required=False)
        parser.add_argument('-j', '--json', metavar='Export to JSON',
                            help="Export to JSON instead of CSV", required=False)
        parser.add_argument('-v', '--version', action='version', version='Order merger 0.1')

        args = vars(parser.parse_args())
        Merger(barcodes_source=args.get('barcodes'),
               orders_source=args.get('orders')).execute(top=int(args.get('top')) if args.get('top') else False,
                                                         output_filename=args.get('filename') if args.get(
                                                             'filename') else 'result',
                                                         json=args.get('json'))
