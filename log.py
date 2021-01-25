import logging


class Log:

    @staticmethod
    def init() -> None:
        logging.basicConfig(
            level = logging.INFO,
            datefmt = '%Y-%m-%d %H:%M:%S',
            format = '%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s'
        )
