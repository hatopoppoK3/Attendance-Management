import secrets

from werkzeug.security import check_password_hash, generate_password_hash

from config import SESSION_LIFETIME, SESSION_LOG_COUNT
from utility.datastore import delete_entity, get_entity, update_entity
from utility.datetime import get_nowdatetime, get_subdatetime
from utility.list import rotate_list_element


class User(object):
    """User Class
    TABLE_NAME : Datastore Name.

    username : str
        ユーザ名(Key値).半角英数字定義.
    userdata : dict
        passhash : str
            passwordから得られるハッシュ値.
        create_time : datetime
            アカウント作成日時.
        login_time : list(datetime)
            ログイン日時.
        logout_time : list(datetime)
            ログアウト日時.
        session_id : str
            セッションID.
    """
    TABLE_NAME = 'testuser'

    def __init__(self, username: str, userdata=None) -> None:
        """
        userクラス初期化メソッド.
        entityよりuserdata初期化.

        Parameters
        ----------
        username : str
            ユーザ名.
        userdata : dict
            ユーザデータ.
        """
        self.username = username
        if userdata is None:
            self.userdata = get_entity(self.TABLE_NAME, username)
        else:
            self.userdata = userdata

    def auth_session(self, session_id: str) -> bool:
        """sessionIDの有効性を検証する.

        Parameters
        ----------
        session_id : str
            認証を行うセッションID

        Returns
        -------
        bool
            session認証ができればTrue.でなければFalse.
        """
        now_datetime = get_nowdatetime()
        sub_datetime = get_subdatetime(
            now_datetime, self.userdata['login_time'][-1])
        if not(self.userdata['session_id'] == session_id) or \
                not(sub_datetime < SESSION_LIFETIME):
            return False

        return True

    def create_user(self, password: str, password_confirm: str) -> bool:
        """ユーザ新規作成メソッド.
        リクエストされるユーザ名が既に存在している場合,
        入力パスワードが異なる場合は作成しない.

        Parameters
        ----------
        password : str
            リクエストされるパスワード.半角英数字.
        password_confirm : str
            確認入力のパスワード.

        Returns
        -------
        bool
            作成できた場合はTrue. それ以外はFalse.
        """
        if not(self.userdata is None) or not(password == password_confirm):
            return False

        self.userdata = {}
        self.userdata['passhash'] = generate_password_hash(password)
        now_datetime = get_nowdatetime()
        self.userdata['create_time'] = now_datetime
        self.userdata['login_time'] = rotate_list_element(now_datetime)
        self.userdata['logout_time'] = []
        self.userdata['session_id'] = secrets.token_hex(64)

        update_entity(self.TABLE_NAME, self.username, self.userdata)

        return True

    def create_session(self, password: str) -> bool:
        """ログイン処理.

        Parameters
        ----------
        password : str
            formの入力password.

        Returns
        ----------
        bool : True or False
            ログイン場合はTrue.
        """
        if (self.userdata is None) or not(
                (check_password_hash(self.userdata['passhash'], password))):
            return False

        self.userdata['login_time'] = rotate_list_element(
            get_nowdatetime(), self.userdata['login_time'], SESSION_LOG_COUNT)
        self.userdata['session_id'] = secrets.token_hex(64)
        update_entity(self.TABLE_NAME, self.username, self.userdata)

        return True

    def delete_user(self, password: str) -> bool:
        if (self.userdata is None) or \
                not(check_password_hash(self.userdata['passhash'], password)):
            return False

        delete_entity(self.TABLE_NAME, self.username)

        return True

    def delete_session(self) -> bool:
        """ログアウト処理.
        セッションIDはNoneにしてDB更新.
        ログアウト日時の更新.

        Returns
        -------
        bool
            ログアウトした場合はTrue. でなければFalse.
        """
        if (self.userdata is None) or \
                not('session_id' in self.userdata.keys()):
            return False

        self.userdata['session_id'] = None
        self.userdata['logout_time'] = rotate_list_element(
            get_nowdatetime(), self.userdata['logout_time'], SESSION_LOG_COUNT)

        update_entity(self.TABLE_NAME, self.username, self.userdata)

        return True
