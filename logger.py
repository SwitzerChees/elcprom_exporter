from utils import get_env_vars
import logging
import os


class Logger:
    def __init__(self) -> None:
        env_vars = get_env_vars()
        self.output_file = env_vars['OUTPUT_FILE']
        if self.output_file != '':
            logging.basicConfig(filename=self.output_file, filemode='w',
                                level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
            print('output_file', self.output_file)

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
