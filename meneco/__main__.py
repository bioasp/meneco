from meneco.meneco import cmd_meneco
import logging

logging.basicConfig(format='%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def main_meneco(args=None):
    cmd_meneco()