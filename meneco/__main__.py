from meneco.meneco import cmd_meneco
import logging
import sys

logging.basicConfig(format='%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


if __name__ == "__main__":
    cmd_meneco(sys.argv[1:])
