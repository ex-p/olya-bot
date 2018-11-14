def safe_index(arr, idx, default=None):
    if len(arr) > idx:
        return arr[idx]
    return default


def put_if_exist(key, value, dst):
    if value:
        dst[key] = value
