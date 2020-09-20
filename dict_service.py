
def increase_or_add_value_to_dict(d: dict, key, value) -> dict:
    if value <= 0:
        return d
    d.update({key: d.get(key, 0) + value})
    return d


def decrease_or_pop_value_from_dict(d: dict, key, value) -> dict:
    new_value = d.get(key, 0) - value
    if new_value <= 0:
        pop_from_dict_if_presented(d, key)
    else:
        d.update({key: new_value})
    return d


def merge_int_dictionaries(d1: dict, d2: dict) -> dict:
    """
    Function that add to first dictionary values of the second (d1[value] = d1[value] + d2[value]) IN-PLACE!
    :param d1:
    :param d2:
    :return:
    """
    for k, v in list(d2.items()):
        d1.update({k: d1.get(k, 0) + v})
    return d1


def pop_from_dict_if_presented(d: dict, key) -> None:
    if isinstance(key, list):
        for k in key:
            try:
                d.pop(k)
            except KeyError:
                pass
    else:
        try:
            d.pop(key)
        except KeyError:
            pass
