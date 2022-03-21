"""
Documention
    https://googleapis.dev/python/datastore/latest/index.html
"""
from google.cloud import datastore
from google.cloud.datastore import Entity, Query

from utility.logging import setup_logger, output_logging

datastore_client = datastore.Client()
datastore_logger = setup_logger(__name__)


def get_table(kind: str) -> Query:
    """テーブル取得メソッド.

    Parameters
    ----------
    kind : str
        取得対象テーブル名.
    Returns
    -------
    Query
        google.cloud.datastore Query

    Raises
    ------
    TypeError
        引数エラーの場合.
    """
    if not(isinstance(kind, str)):
        message = 'TypeError at get_table method'
        output_logging(datastore_logger, 'alert', message)
        raise TypeError(message)
    query = datastore_client.query(kind=kind)

    return query.fetch()


def update_table(kind: str, data: dict) -> None:
    """テーブル更新メソッド.

    Parameters
    ----------
    kind : str
        更新対象テーブル名.
    data : dict
        更新データ.
    Raises
    ------
    TypeError
        引数エラーの場合.
    """
    if not(isinstance(kind, str) or isinstance(data, dict)):
        message = 'TypeError at update_table method'
        output_logging(datastore_logger, 'alert', message)
        raise TypeError(message)

    entity_list = []
    for id_or_name, value in data.items():
        entity = datastore.Entity(
            key=datastore_client.key(kind, id_or_name))
        entity.update(value)
        entity_list.append(entity)

        # データ長が400超える場合はエラーになるため,一度put.
        if len(entity_list) == 400:
            datastore_client.put_multi(entity_list)
            entity_list.clear()

    datastore_client.put_multi(entity_list)


def delete_table(kind: str) -> None:
    """テーブル削除メソッド.

    Parameters
    ----------
    kind : str
        削除対象テーブル名.

    Raises
    ------
    TypeError
        引数エラーの場合.
    """
    if not(isinstance(kind, str)):
        message = 'TypeError at delete_table method'
        output_logging(datastore_logger, 'alert', message)
        raise TypeError(message)

    table = get_table(kind)
    key_list = []
    for data in table:
        key_list.append(data.key)

        # データ長が400超える場合はエラーになるため,一度delete.
        if len(key_list) == 400:
            datastore_client.delete_multi(key_list)
            key_list.clear()

    datastore_client.delete_multi(key_list)


def get_entity(kind: str, id_or_name: str) -> Entity:
    """エンティティ取得メソッド.

    Parameters
    ----------
    kind : str
        取得対象テーブル名.
    id_or_name : str
        取得対象エンティティ名.

    Returns
    -------
    Entity
        google.cloud.datastore Entity

    Raises
    ------
    TypeError
        引数エラーの場合.
    """
    if not(isinstance(kind, str) or isinstance(id_or_name, str)):
        message = 'TypeError at get_entity method'
        output_logging(datastore_logger, 'alert', message)
        raise TypeError(message)

    return datastore_client.get(datastore_client.key(kind, id_or_name))


def update_entity(kind: str, id_or_name: str, data: dict) -> None:
    """エンティティ更新メソッド.

    Parameters
    ----------
    kind : str
        更新対象テーブル名.
    id_or_name : str
        更新対象エンティティ名.
    data : dict
        更新データ.

    Raises
    ------
    TypeError
        引数エラーの場合.
    """
    if not(isinstance(kind, str) or
           isinstance(id_or_name, str) or isinstance(data, dict)):
        message = 'TypeError at update_entity method'
        output_logging(datastore_logger, 'alert', message)
        raise TypeError(message)

    entity = datastore.Entity(
        key=datastore_client.key(kind, id_or_name))
    entity.update(data)
    datastore_client.put(entity)


def delete_entity(kind: str, id_or_name: str) -> None:
    """エンティティ削除メソッド.

    Parameters
    ----------
    kind : str
        削除対象テーブル名.
    id_or_name : str
        削除対象エンティティ名.

    Raises
    ------
    TypeError
        引数エラーの場合.
    """
    if not(isinstance(kind, str) or isinstance(id_or_name, str)):
        message = 'TypeError at delete_entity method'
        output_logging(datastore_logger, 'alert', message)
        raise TypeError(message)

    entity = get_entity(kind, id_or_name)
    if entity is None:
        pass
    else:
        datastore_client.delete(entity.key)
