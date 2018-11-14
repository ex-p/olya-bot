def safe_index(arr, idx, default=None):
    if len(arr) > idx:
        return arr[idx]
    return default
