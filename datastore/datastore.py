"""
Documention
    https://googleapis.dev/python/datastore/latest/index.html
"""
from google.cloud import datastore
from google.cloud.datastore import Entity, Query

datastore_client = datastore.Client()


def get_table(kind: str) -> Query:
    """テーブル取得.

    Parameters
    ----------
    kind : str
        種別.

    Returns
    -------
    Query
        google.cloud.datastore Query
    """

    query = datastore_client.query(kind=kind)

    return query.fetch()


def update_table(kind: str, data: dict) -> None:
    """テーブル更新.

    Parameters
    ----------
    kind : str
        種別.

    data : dict
        更新データ.
    """

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
    """テーブル削除.

    Parameters
    ----------
    kind : str
        種別.
    """

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
    """エンティティ取得.

    Parameters
    ----------
    kind : str
        種別.

    id_or_name : str
        エンティティキー.

    Returns
    -------
    Entity
        google.cloud.datastore Entity
    """

    return datastore_client.get(datastore_client.key(kind, id_or_name))


def update_entity(kind: str, id_or_name: str, data: dict) -> None:
    """エンティティ更新.

    Parameters
    ----------
    kind : str
        種別.

    id_or_name : str
        エンティティキー.

    data : dict
        更新データ.
    """

    entity = datastore.Entity(
        key=datastore_client.key(kind, id_or_name))
    entity.update(data)
    datastore_client.put(entity)


def delete_entity(kind: str, id_or_name: str) -> None:
    """エンティティ削除.

    Parameters
    ----------
    kind : str
        種別.

    id_or_name : str
        エンティティキー.
    """

    entity = get_entity(kind, id_or_name)
    if entity is None:
        pass
    else:
        datastore_client.delete(entity.key)
