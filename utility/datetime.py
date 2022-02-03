import datetime


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
