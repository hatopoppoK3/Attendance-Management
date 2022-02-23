import functools
from secrets import compare_digest, token_hex

from flask import g, redirect, session, url_for

from config import TOKEN_LENGTH


def login_required(func):
    @functools.wraps(func)
    def wrapper(**kwargs):
        if g.session:
            return func(**kwargs)

        return redirect(url_for('session.login.show_login'))

    return wrapper


def create_session(func):
    """sessionIDを作成し、グローバル変数gとcookie sessionに格納する.

    """
    @functools.wraps(func)
    def wrapper(**kwargs):
        session_id = token_hex(TOKEN_LENGTH)
        session['session_id'] = session_id
        g.session_id = session_id
        return func(**kwargs)

    return wrapper


def auth_session(session_id: str) -> bool:
    """cookie sessionにあるsessionIDと引数sessionIDを比較する.

    Parameters
    ----------
    session_id : str
        認証するsessionID.

    Returns
    -------
    bool
        認証ができればTrue.cookieにsession_idがない場合,異なる場合はFalse

    Raises
    ------
    ValueError
        引数がstrでない場合
    """
    # 関数引数チェック
    if not(type(session_id) == str):
        raise ValueError('入力引数エラー')

    if not('session_id' in session.keys()):
        return False

    return compare_digest(session['session_id'], session_id)
