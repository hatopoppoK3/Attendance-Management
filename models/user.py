from werkzeug.security import check_password_hash, generate_password_hash

from config import SESSION_LOG_COUNT, USER_TABLE
from utility.datastore import delete_entity, get_entity, update_entity
from utility.datetime import convert_datetime_tostring, get_nowdatetime
from utility.list import rotate_list_element


class User(object):
    """User Class
    TABLE_NAME : Datastore Name.

    username : str
        ユーザ名(Key値).半角英数字定義.
    userdata : dict
        passhash : str
            (password)+(create_time(YYYY/mm/dd/HH/MM/SS/ffffff))から得られるハッシュ値.
        create_time : datetime
            アカウント作成日時.
        login_time : list(datetime)
            ログイン日時.
        logout_time : list(datetime)
            ログアウト日時.
    """

    def __init__(self, username: str) -> None:
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
        self.userdata = get_entity(USER_TABLE, username)

    def create_user(self, password: str, password_confirm: str) -> bool:
        """ユーザ新規作成メソッド.
        リクエストされるユーザ名が既に存在している場合,
        入力パスワードが異なる場合は作成しない.
        hashは(password)+(作成日時(YYYY/mm/dd/HH/MM/SS/ffffff))で作成する.

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
        now_datetime = get_nowdatetime()
        input_str = password+convert_datetime_tostring(now_datetime)
        self.userdata['passhash'] = generate_password_hash(input_str)
        self.userdata['create_time'] = now_datetime
        self.userdata['login_time'] = rotate_list_element(now_datetime)
        self.userdata['logout_time'] = []

        update_entity(USER_TABLE, self.username, self.userdata)

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
        if (self.userdata is None):
            return False

        input_str = password + \
            convert_datetime_tostring(self.userdata['create_time'])
        if not((check_password_hash(self.userdata['passhash'], input_str))):
            return False

        self.userdata['login_time'] = rotate_list_element(
            get_nowdatetime(), self.userdata['login_time'], SESSION_LOG_COUNT)
        update_entity(USER_TABLE, self.username, self.userdata)

        return True

    def delete_user(self, password: str) -> bool:
        if (self.userdata is None):
            return False
        input_str = password + \
            convert_datetime_tostring(self.userdata['create_time'])
        if not(check_password_hash(self.userdata['passhash'], input_str)):
            return False

        delete_entity(USER_TABLE, self.username)

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
        if (self.userdata is None):
            return False

        self.userdata['logout_time'] = rotate_list_element(
            get_nowdatetime(), self.userdata['logout_time'], SESSION_LOG_COUNT)

        update_entity(USER_TABLE, self.username, self.userdata)

        return True


class UserException(Exception):
    def __init__(self, comment: str, level: str):
        self.comment = comment
        self.level = level

    def __str__(self) -> str:
        return f'comment:{self.comment}, level:{self.level}'
