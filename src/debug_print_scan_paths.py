def debug_print(results):
    """
    Print the scan results for each user.
    used for scan_paths.py
    Parameters:
    results (dict): A dictionary containing user IDs as keys and their corresponding paths and existence status as values.
    """
    for user_id, paths in results.items():
        print(f"Results for user ID {user_id}:")
        for path, exists in paths.items():
            if '{}' in path:
                print(f"  {path}: {'Exists' if exists else 'Does not exist'}")
            else:
                print(f"  {path}: {exists}")