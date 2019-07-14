import logging

from utils import CSV, DEBUG


class Merger:
    def __init__(self, barcodes_source, orders_source,
                 orders_customer_index=1, orders_order_index=0, barcodes_barcode_index=0, barcodes_order_index=1):

        self._logging = logging.getLogger(__name__)
        self._barcodes = CSV(barcodes_source).read()
        self._orders = CSV(orders_source).read()

        self._indexes = {
            'orders_customer': orders_customer_index,
            'orders_order': orders_order_index,
            'barcodes_barcode': barcodes_barcode_index,
            'barcodes_order': barcodes_order_index,
        }
        self._customers = set([order[orders_customer_index] for order in self._orders])

    def __logger__(self, level, message):
        """
        Python standart logger wrapper.
        had to implement something fast in order to separate the log file from the output.
        :param level: for the time being; debug error and info for the rest.
        :param message: string
        :return: void.
        """

        if level.lower() == 'debug' and DEBUG:
            self._logging.debug(message)
            print(message)
        elif level.lower() == 'error':
            self._logging.error(message)
        elif level.lower() == 'info':
            self._logging.info(message)
            print(message)

    def __map_customers_orders__(self):
        """
        Creates a dictionary for the customers orders
        :return: Mapped version of the first data source
        Example: { customer: [order_id_1, order_id_2, order_id_3] }
        """

        mapped = {}  # TODO: Figure out a better name

        for customer in self._customers:
            mapped[customer] = []
            [mapped[customer].append(order[self._indexes['orders_order']]) if customer == order[
                self._indexes['orders_customer']] else None for order in self._orders]
        self.__logger__('debug', mapped)
        return mapped

    def __map_orders_barcodes__(self):
        """
        Creates a dictionary for what orders used what barcodes based on the barcodes data source.
        In addition catch all empty barcodes, not used barcodes and barcodes that been repeated.
        :return: Mapped version
        Example: {order_id: [barcode_1, barcode_2, barcode_3]}
        """
        all_barcodes = [barcode[self._indexes['barcodes_barcode']] for barcode in self._barcodes]

        def validator(entry):
            """
            Easy to extend validator that runs for every entry as part of the map iteration and throw a exception.
            :param entry: [barcode, order]
            :return: void
            """
            barcode, order = entry[self._indexes['barcodes_barcode']], entry[self._indexes['barcodes_order']]
            if all_barcodes.count(barcode) > 1:
                raise ValueError(
                    'Barcode:{} appears in the source {} times'.format(barcode, all_barcodes.count(barcode)))
            if not barcode:
                raise ValueError("Order id:{} doesn't have a barcode".format(order))

        mapped, unused = {}, []
        for item in self._barcodes:
            if item[self._indexes['barcodes_order']]:
                try:
                    validator(item)
                    if type(mapped.get(item[self._indexes['barcodes_order']])) is list:
                        mapped[item[self._indexes['barcodes_order']]].append(item[self._indexes['barcodes_barcode']])
                    else:
                        mapped[item[self._indexes['barcodes_order']]] = [item[self._indexes['barcodes_barcode']]]
                except ValueError as e:
                    self.__logger__('error', e)
            else:
                unused.append(item[self._indexes['barcodes_barcode']])

        unused_msg = '# There are {} unused barcodes #'.format(unused.__len__())
        self.__logger__('info', '#' * len(unused_msg))
        self.__logger__('info', unused_msg)
        self.__logger__('info', '#' * len(unused_msg))
        self.__logger__('debug', mapped)
        return mapped

    def __merge_it__(self, mapped_orders, mapped_barcodes):
        """
        Merging both dictionaries into a lovely one
        :param mapped_orders: pretty self explanatory
        :param mapped_barcodes: also self explanatory
        :return: a final merged version
        """
        final = {}
        for customer in self._customers:
            final[customer] = {}
            if mapped_orders.get(customer):
                for order in mapped_orders.get(customer):
                    final[customer][order] = mapped_barcodes.get(order) if mapped_barcodes.get(order) else None
            else:
                self.__logger__('info', 'No orders for customer:{}'.format(customer))
        self.__logger__('debug', final)
        return final

    def execute(self, top=False, output_filename='result', json=False):
        """
        The executor
        :param output_filename: default: 'result'
        :param top: a integer which returns the top users base on the amount of orders they made (top 3 orders for example)
        :param output:
        :return:
        """

        self.__logger__('info', "Let's do this!")
        mapped_orders, mapped_barcodes = self.__map_customers_orders__(), self.__map_orders_barcodes__()
        merged = self.__merge_it__(mapped_orders, mapped_barcodes)

        if top:
            orders_per_customer = sorted(mapped_orders.items(),
                                         key=lambda item: len(item[self._indexes['orders_customer']]))
            self.__logger__('debug', orders_per_customer)

            top_customers = dict(orders_per_customer[-top:])
            top_msg = 'Our top {top_num} customers are:'.format(top_num=top)
            self.__logger__('info', top_msg)
            self.__logger__('info', '=' * len(top_msg))
            [self.__logger__('info', ' * Customer:{} with {} orders'.format(customer, len(orders))) for customer, orders
             in top_customers.items()]

        self.__logger__('info', CSV(output_filename).write(merged, to_json=json))
        self.__logger__('info', 'fin.')
