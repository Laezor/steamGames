import os


def get_steam_library_folders(steam_path):
    """
    This function reads the 'libraryfolders.vdf' file from the Steam installation directory to extract the paths of all Steam library folders.

    Parameters:
    steam_path (str): The path to the Steam installation directory.

    Returns:
    list: A list of paths to all Steam library folders.
    """
    library_folders_path = os.path.join(steam_path, 'steamapps', 'libraryfolders.vdf')
    with open(library_folders_path, 'r') as file:
        data = file.read()

    # Extract library paths from the VDF file
    library_paths = []
    for line in data.splitlines():
        if 'path' in line:
            path = line.split('"')[3]
            library_paths.append(path)

    return library_paths

def get_installed_games(library_paths):
    """
    This function goes through each Steam library path to find all installed games. It does this by looking for files that start with 'appmanifest_' and end with '.acf' in the 'steamapps' directory within each library path. These files contain information about the games, so the function reads them to extract the game's name, Steam ID, and installation directory. It stores this information in a list and returns it at the end.
    
    Parameters:
    library_paths (list): A list of paths to the Steam library folders.
    
    Returns:
    list: A list of dictionaries, each containing information about an installed game.
    """
    games = []
    for path in library_paths:
        steamapps_path = os.path.join(path, 'steamapps')
        for file_name in os.listdir(steamapps_path):
            if file_name.startswith('appmanifest_') and file_name.endswith('.acf'):
                appmanifest_path = os.path.join(steamapps_path, file_name)
                with open(appmanifest_path, 'r') as file:
                    data = file.read()

                # Extract game name and Steam ID from the ACF file
                game_info = {}
                for line in data.splitlines():
                    if 'appid' in line:
                        game_info['appid'] = line.split('"')[3]
                    if 'name' in line:
                        game_info['name'] = line.split('"')[3]
                    if 'installdir' in line:
                        game_info['installdir'] = line.split('"')[3]
                if game_info:
                    games.append(game_info)

    return games