import logging

logging.basicConfig(level=logging.INFO,
                    format=format('T: %(asctime)s | LVL: %(levelname)s | Func: %(funcName)s | L: '
                                  f'%(lineno)s | | MSG: %(message)s - %(name)s||\n{("-" * 150)}'),
                    datefmt='%H:%M:%S')
logger = logging.getLogger()
