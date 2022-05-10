import logging
import time
from configparser import ConfigParser

from orchestrator import Orchestrator
from settings import get_workers
from show import show

logging.basicConfig(filename='main.log',
                    filemode='w',
                    format='%(asctime)s: %(levelname)s: %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger("Top GitHub")

for key in logging.Logger.manager.loggerDict:
    if key != "Top GitHub":
        logging.getLogger(key).setLevel(logging.CRITICAL)

if __name__ == "__main__":
    config = ConfigParser()
    config.read("config.ini")

    modes = ["default", "thread", "process", "async"]

    performance = {}
    logger.debug(f"Number of organizations: {config['GitHub']['number_of_organization']}")
    for mode in modes:
        logger.debug("=" * 50)
        config["Build"]["mode"] = mode
        logger.debug(f"Start pipeline with {mode = }")
        workers = get_workers(config)
        start = time.time()
        Orchestrator.run(workers)
        performance[mode] = round(time.time() - start, 2)
        logger.debug(f"Elapsed time is {performance[mode]} seconds.")

    # выводит в консоль
    show()

    logger.debug(f"Results for each mode:\n{performance}")
