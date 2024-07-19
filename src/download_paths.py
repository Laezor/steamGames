import asyncio
import json
import os
import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from get_installed_games import get_installed_games, get_steam_library_folders

from global_funcs import  get_request, get_steam_path, get_ubisoft_path, remove_extension_and_filename

load_dotenv()


def split_path_by_placeholders(original_save_path):
    """
    This function takes a path as input and checks if it contains any of the known placeholders for environment variables. 
    If it finds a placeholder, it splits the path at that point and reassembles it with the placeholder in its original position. 
    This is done to ensure the path is correctly formatted for further processing.
    
    Parameters:
    original_save_path (str): The path to be processed.
    
    Returns:
    str: The processed path with placeholders correctly formatted.
    """
    placeholders = ['%LOCALAPPDATA%', '%USERPROFILE%', '%APPDATA%']
    for placeholder in placeholders:
        if placeholder in original_save_path:
            original_save_path = original_save_path.split(placeholder)[0] + placeholder + original_save_path.split(placeholder)[1]
            break
    return original_save_path
        
def clean_path(original_save_path):
    """
    This function takes a path as input and cleans it up by removing certain unwanted parts. 
    It first removes any text enclosed in square brackets, then removes the file extension and filename, 
    followed by removing any trailing asterisks, and finally removes the string "loop_save" if present. 
    The cleaned path is then returned.
    
    Parameters:
    original_save_path (str): The path to be cleaned.
    
    Returns:
    str: The cleaned path.
    """
    clean_save_path = re.sub(r'\[.*?\]', '', original_save_path).strip()
    clean_save_path = remove_extension_and_filename(clean_save_path).strip()
    clean_save_path = re.sub(r"\*$", '', clean_save_path).strip()
    clean_save_path = re.sub(r"loop_save", '', clean_save_path).strip()
    return clean_save_path

async def get_pcgamingwiki_save_path(appid):
    url = f"https://pcgamingwiki.com/api/appid.php?appid={appid}"
    response = await get_request(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    save_game_section = soup.find('span', id='Save_game_data_location')
    if not save_game_section:
        return None

    rows = save_game_section.find_next('table').find_all('tr', class_='template-infotable-body table-gamedata-body-row')

    save_paths = []
    for row in rows:
        platform = row.find('th', class_='table-gamedata-body-system')
        if not platform or platform.text.strip().lower() not in ['steam', 'windows']:
            continue
        save_path = row.find('td', class_='table-gamedata-body-location')
        if save_path:
            original_save_path = save_path.text.strip()
            original_save_path = split_path_by_placeholders(original_save_path)
            clean_save_path = clean_path(original_save_path)
            if clean_save_path:
                save_paths.append(clean_save_path)

    return save_paths if save_paths else None

def paths_to_json(data):
    """
    This function takes a list of data and writes it to a JSON file named 'steam_paths.json'.
    
    Parameters:
    data (list): The data to be written to the JSON file.
    """
    with open('steam_paths.json', 'w') as f:
        print(data)
        json.dump(data, f)
        f.write('\n')


async def dump_to_json(installed_games):
    steam_path = get_steam_path()
    path_to_game = os.environ.get("path_to_game")
    ubisoft_path = get_ubisoft_path()

    data = []
    tasks = []
    for game in installed_games:
        tasks.append(get_pcgamingwiki_save_path(game['appid']))

    results = await asyncio.gather(*tasks)

    for game, pcgamingwiki_paths in zip(installed_games, results):
        if pcgamingwiki_paths:
            for path in pcgamingwiki_paths:
                formatted_path = path.replace('<user-id>', '{}').replace('<Steam-folder>', steam_path).replace('<Ubisoft-Connect-folder>', ubisoft_path).replace('<path-to-game>', f'{steam_path}{path_to_game}\\\\{game["installdir"]}')
                data.append({
                    'appid': game['appid'],
                    'path': formatted_path
                })

    paths_to_json(data)

def main():
    # Replace this with your actual Steam installation path
    steam_path =  get_steam_path()
    library_paths = get_steam_library_folders(steam_path)
    installed_games = get_installed_games(library_paths)
    asyncio.run(dump_to_json(installed_games))


if __name__ == "__main__":
    main()