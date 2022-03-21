import logging


def setup_logger(logger_name: str) -> logging.Logger:
    """Loggerの作成メソッド.

    Parameters
    ----------
    logger_name : str
        __name__を推奨.

    Returns
    -------
    logging.Logger
        作成したlogger.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    logger_handler = logging.StreamHandler()
    logger_formatter = logging.Formatter(
        '%(asctime)s - [%(levelname)s] - %(name)s : %(message)s',
        '%Y-%m-%d %H:%M:%S')
    logger_handler.setFormatter(logger_formatter)

    logger.addHandler(logger_handler)

    return logger


def output_logging(logger: logging.Logger, level: str, message: str) -> None:
    """ログ出力.

    Parameters
    ----------
    logger : logging.Logger
        setup_loggerで作成したlogger.
    level : str
        'info' or 'warning' or 'alert' いずれかを指定.
    message : str
        message部.

    Raises
    ------
    TypeError
        引数エラー.
    ValueError
        未定義レベルの指定.
    """
    if not(isinstance(logger, logging.Logger) or
           isinstance(level, str) or isinstance(message, str)):
        raise TypeError('TypeError at output_logging method')
    if (level == 'info') or (level == 'success'):
        logger.info(message)
    elif level == 'warning':
        logger.warning(message)
    elif level == 'alert':
        logger.error(message)
    else:
        raise ValueError('未定義level')
