import json, os, platform
import httpx


def check_system_architecture():
    """
    This function determines the system architecture by retrieving the primary architecture type from the platform module.

    Returns:
    str: The primary system architecture type.
    """
    architecture = platform.architecture()[0]
    
    return architecture

def expand_environment_variables(path):
    """
    This function expands any environment variables present in the provided path.

    Parameters:
    path (str): The path containing environment variables to be expanded.

    Returns:
    str: The path with expanded environment variables.
    """
    return os.path.expandvars(path)

def read_paths_from_file(file_path):
    """
    This function reads the paths from a JSON file.

    Parameters:
    file_path (str): The path to the JSON file containing the paths.

    Returns:
    list: A list of paths extracted from the JSON file.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
        paths = [d['path'] for d in data]

    return paths

def read_appids_from_file(file_path):
    """
    This function reads the appids from a JSON file and returns them as a list.

    Parameters:
    file_path (str): The path to the JSON file containing the appids.

    Returns:
    list: A list of appids extracted from the JSON file.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
        appids = [d['appid'] for d in data]

    return appids

def read_appids_paths_from_file(file_path):
    """
    This function reads the appids and their corresponding paths from a JSON file and returns them as a dictionary.

    Parameters:
    file_path (str): The path to the JSON file containing the appids and paths.

    Returns:
    dict: A dictionary where the keys are the expanded paths and the values are the corresponding appids.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
        appid_paths = {expand_environment_variables(d['path']): d['appid'] for d in data}
    return appid_paths

def remove_extension_and_filename(path):
    """
    This function takes a path as input and returns the directory if the path has an extension, otherwise returns the original path.

    Parameters:
    path (str): The path to be processed.

    Returns:
    str: The directory if the path has an extension, otherwise the original path.
    """
    # Split the path into directory and filename
    directory, filename = os.path.split(path)

    # Split the filename into root and extension
    root, ext = os.path.splitext(filename)

    # Check if there is an extension
    if ext:
        return directory
    else:
        return path

def get_correct_path(path):
    """
    This function determines the correct path based on whether the input path points to a file or a directory.

    Parameters:
    path (str): The input path to be evaluated.

    Returns:
    str: The directory containing the file if the input path points to a file, otherwise returns the original path.
    """
    if os.path.isfile(path):
        return os.path.dirname(path)
    else:
        return path
    
def get_steam_path():
    """
    Determine the Steam installation path based on the system architecture and custom settings.

    Returns:
    str: The path to the Steam installation directory.
    """
    plat = check_system_architecture()
    custom_steam_path = os.environ.get("custom_steam_path")
    
    if custom_steam_path == "":
        if plat == "64bit":
            steam_path = os.environ.get("steam_path64")
        else:
            steam_path = os.environ.get("steam_path32")
    else:
        steam_path = custom_steam_path

    return steam_path

def get_ubisoft_path():
    """
    Determine the Ubisoft Connect installation path based on the system architecture and custom settings.

    Returns:
    str: The path to the Ubisoft Connect installation directory.
    """
    plat = check_system_architecture()
    custom_ubisoft_path = os.environ.get("custom_ubisoft_path")
    
    if custom_ubisoft_path == "":
        if plat == "64bit":
            ubisoft_path = os.environ.get("ubisoft_connect_path64")
        else:
            ubisoft_path = os.environ.get("ubisoft_connect_path32")
    else:
        ubisoft_path = custom_ubisoft_path

    return ubisoft_path

async def get_request(url):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
    except httpx.RequestError as e:
        print(f"Error fetching data for {url}: {e} {response.status_code} {response.reason_phrase}")
        return None
    return response