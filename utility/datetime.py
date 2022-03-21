import datetime

from utility.logging import setup_logger, output_logging

datetime_logger = setup_logger(__name__)


def get_nowdatetime() -> datetime.datetime:
    """
    JST日本時刻をdatetime型で取得.

    Returns
    -------
    datetime.datetime
        日本時間での現在時刻.
    """
    jst_timezone = datetime.timezone(datetime.timedelta(hours=9))
    return datetime.datetime.now(tz=jst_timezone)


def convert_datetime_tostring(target_datetime: datetime.datetime,
                              date_only=False) -> str:
    """datetime型をstr型に変換する.
    date_only=Trueの場合はYYYY-mm-dd.
    date_only=False(default)の場合はYYYY-mm-dd HH:MM:SS:ffffff.

    Parameters
    ----------
    target_datetime : datetime.datetime
        変換対象のdatetime.
    date_only : bool, optional
        日付のみの場合はTrue, by default False

    Returns
    -------
    str
        YYYY-mm-dd HH:MM:SS:FFFFFF.

    Raises
    ------
    TypeError
        引数エラー.
    """
    if not(isinstance(target_datetime, datetime.datetime) or
           isinstance(date_only, bool)):
        message = 'TypeError at convert_datetime_tostring method'
        output_logging(datetime_logger, 'alert', message)
        raise TypeError(message)

    target_datetime = target_datetime.astimezone(
        datetime.timezone(datetime.timedelta(hours=9)))
    if date_only:
        return target_datetime.strftime('%Y-%m-%d')
    return target_datetime.strftime('%Y-%m-%d %H:%M:%S:%f')


def get_subdatetime(time1: datetime.datetime,
                    time2: datetime.datetime) -> int:
    """time1-time2の結果を秒単位で取得する.

    Parameters
    ----------
    time1 : datetime.datetime
        引かれる数.
    time2 : datetime.datetime
        引く数.

    Returns
    -------
    int
        秒単位で結果を返す.小数点切り捨て.
    """
    return int((time1-time2).total_seconds())
