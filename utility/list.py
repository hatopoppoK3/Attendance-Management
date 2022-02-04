def rotate_list_element(element, target_list=[], length=1) -> list:
    """要素をリストに追加する.
    追加先リストを指定しない場合はelementのみの長さ1のリストを返す.
    target_listが既にlengthを超えている場合はelementを追加した後に,
    listの長さがlengthになるまで古い要素を削除して返す.

    Parameters
    ----------
    element
        リストに追加する要素
    target_list : list, optional
        要素の追加先のlist, by default []
    length : int, optional
        指定長までリストの要素を削除する, by default 1

    Returns
    -------
    list
        element追加してlength以下の長さのlist.

    Raises
    ------
    TypeError
        引数エラーの場合.
    ValueError
        lengthが1未満の場合.
    """
    # 入力引数の型が異なる場合は例外発生.
    if not(type(target_list) == list) or not(type(length) == int):
        raise TypeError('入力引数の型エラー')
    elif length < 1:
        raise ValueError('リスト長エラー')

    target_list.append(element)
    # lengthの長さ以下になるように古い要素から捨てる.
    for cnt in range(0, len(target_list)-length):
        target_list.pop(0)

    return target_list
