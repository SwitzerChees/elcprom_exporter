import argparse
import logging
import os


class Logger:
    def __init__(self) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument('--log_file', default='',
                            help='Thes file where the logs get stored. If no file set, no log file is written')
        args = vars(parser.parse_known_args()[0])
        self.log_file = args['log_file']
        dir_path = os.path.abspath(os.path.dirname(__file__))
        if self.log_file != '':
                logging.basicConfig(filename=os.path.join(
                    dir_path, self.log_file), filemode='w', level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')


    def info(self, msg, do_print=True):
        msg = str(msg)
        logging.info(msg)
        if do_print:
            print(msg)

    def error(self, msg, do_print=True):
        msg = str(msg)
        logging.error(msg)
        if do_print:
            print(msg)