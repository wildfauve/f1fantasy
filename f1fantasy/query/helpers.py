def single_result_or_none(result):
    result_list = list(result)
    if len(result_list) != 1:
        return None
    return result_list[0]
