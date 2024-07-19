import os
from dotenv import load_dotenv
import json
from debug_print_scan_paths import debug_print

from global_funcs import read_appids_paths_from_file, read_paths_from_file, expand_environment_variables
load_dotenv()

def check_paths(user_ids, paths_file):
    """
    This function checks the existence of paths for a given list of user ids.
    
    It first reads the paths from a file, then expands any environment variables in the paths.
    For each user id, it checks the existence of each path and stores the results in a dictionary.
    
    Parameters:
    user_ids (list): A list of user ids to check paths for.
    paths_file (str): The file containing the paths to check.
    
    Returns:
    dict: A dictionary where the keys are user ids and the values are dictionaries of paths and their existence.
    """
    paths = read_paths_from_file(paths_file)

    # Expand environment variables in paths
    paths = [os.path.expandvars(path) for path in paths]

    results = {}
    for user_id in user_ids:
        user_results = {}
        for path in paths:
            formatted_path = path.format(user_id)
            user_results[formatted_path] = os.path.exists(formatted_path)
        results[user_id] = user_results

    return results


def dump_results_to_file(results, output_file):
    """
    This function takes the results of the path checks and writes them to a file in JSON format.
    
    It first initializes an empty list to hold the data and a set to keep track of unique paths. Then, it reads the paths associated with appids from a file. For each user id in the results, it iterates over the appid paths, expands the environment variables in the paths, and checks if the path exists. If the path exists and hasn't been seen before, it adds the path and its corresponding appid to the data list. Finally, it writes the data to the specified output file in JSON format with indentation for readability.
    
    Parameters:
    results (dict): A dictionary containing the results of the path checks.
    output_file (str): The file where the results will be written.
    """
    data = []
    seen_paths = set()  # To keep track of unique paths

    # Read appid paths from file once
    appid_paths = read_appids_paths_from_file('steam_paths.json')

    for user_id in results.keys():
        for path, appid in appid_paths.items():
            expanded_path = expand_environment_variables(path).format(user_id)
            if expanded_path not in seen_paths and os.path.exists(expanded_path):
                seen_paths.add(expanded_path)
                data.append({'appid': appid, 'path': expanded_path})

    # Write data to the output file
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)  # Optional: indent for readability

def main():
    # Example usage
    user_ids = [f'{os.environ.get("steam_user_id")}', f'{os.environ.get("steam_acc_id")}',
                f'{os.environ.get("ubisoft_user_id")}']
    paths_file = 'steam_paths.json'
    output_file = 'steam_paths_final.json'
    results = check_paths(user_ids, paths_file)
    #uncomment this only for debugging
    debug_print(results)

    dump_results_to_file(results, output_file)


if __name__ == '__main__':
    main()