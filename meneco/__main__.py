import logging
import sys

from meneco.meneco import cmd_meneco

logging.basicConfig(format="%(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def main_meneco(args=None):
    cmd_meneco(sys.argv[1:])


if __name__ == "__main__":
    main_meneco()
